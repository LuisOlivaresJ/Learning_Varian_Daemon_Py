"""
Set up our Storage Service Class Provider (SCP)

This script should be executed in a separate terminal.

----- Linux Service with systemd (optional) ----

    The file /Linux_SCP_service/my_scp_pynetdicom.service is
    an example of a service in Linux that executes this script
    automatically.

    - Copy the file to:
        /etc/systemd/system/

    - In a terminal, run these commands
        $ sudo systemctl daemon-reload
        $ sudo systemctl start my_scp_pynetdicom.service
        $ sudo systemctl status my_scp_pynetdicom.service 

"""

import os
from pathlib import Path
import signal
import logging
import sys

from pynetdicom import AE, build_context, evt

from dotenv import load_dotenv


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("My DICOM-SCP")

# Load environment variables (AE Title, IP, Port)
load_dotenv()  # This loads the variables from .env file

VarianDB_PORT = os.getenv("VARIAN_DB_PORT")
VarianDB_AET = os.getenv("VARIAN_DB_AET")
VarianDB_IP = os.getenv("VARIAN_DB_IP")

SCP_IP = os.getenv("PyNetDICOM_SCP_IP")
SCP_PORT = os.getenv("PyNetDICOM_SCP_PORT")
SCP_AET = os.getenv("PyNetDICOM_SCP_IP_AET")

# SOP Classes used in Presentation Context
## Study Root Query/Retrieve Move
STUDY_ROOT_QR_MOVE = "1.2.840.10008.5.1.4.1.2.2.2"
## SOP Class UID
RT_IMAGE_CLASS_UID = "1.2.840.10008.5.1.4.1.1.481.1"


MY_PATH_TO_DICOM_STORAGE_DIRECTORY = "/home/luis/FM/testing_DICOM_C-MOVE"


# Implement the handler for evt.EVT_C_SMY_PATH_TO_DICOM_STORAGE_DIRECTORYTORE
def handle_store(event):
    """Handle a C-STORE request event."""
    ds = event.dataset
    ds.file_meta = event.file_meta

    # Save the dataset using the SOP Instance UID as the filename
    path_to_save = Path(MY_PATH_TO_DICOM_STORAGE_DIRECTORY) / ds.SOPInstanceUID
    ds.save_as(path_to_save, enforce_file_format=True)

    # Return a 'Success' status
    return 0x0000

handlers = [(evt.EVT_C_STORE, handle_store)]

# Create an Application Entity
ae = AE(SCP_AET)  # AE Title
ae.add_requested_context(STUDY_ROOT_QR_MOVE)  # C-MOVE
ae.add_requested_context(RT_IMAGE_CLASS_UID)  # RT Image SOP Class

# --- Graceful shutdown handler ---
# Shutdown the SCP when the service stop (SIGTERM or SIGINT signals from the OS)
def shutdown_handler(signum, frame):
    logger.info(f"Shutdown signal received {signum}. Stopping SCP...")
    ae.shutdown()
    sys.exit(0)

signal.signal(signal.SIGTERM, shutdown_handler)
signal.signal(signal.SIGINT, shutdown_handler)  # Ctrl+C sends SIGINT



def main():
    logger.info("Starting DICOM Storage SCP")

    # Define the presentation contexts for the Storage SCP
    contexts = [build_context(RT_IMAGE_CLASS_UID)]

    # Start our Storage SCP in non-blocking mode
    ae.start_server(
        address=(SCP_IP, int(SCP_PORT)),
        evt_handlers=handlers,
        contexts=contexts,
        block = True
    )

if __name__ == "__main__":
    main()