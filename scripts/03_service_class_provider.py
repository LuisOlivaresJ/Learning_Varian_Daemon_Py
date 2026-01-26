"""
This script should be ejecuted as a service in our server.


"""

import os
from pathlib import Path

from pynetdicom import AE, build_context, evt

from dotenv import load_dotenv


# Load environment variables (AE Title, IP, Port)
load_dotenv()  # This loads the variables from .env file
VarianDB_PORT = os.getenv("VARIAN_DB_PORT")
VarianDB_AET = os.getenv("VARIAN_DB_AET")
VarianDB_IP = os.getenv("VARIAN_DB_IP")

PyNETDICOM_IP = os.getenv("PYNETDICOM_IP")
PyNETDICOM_AET = os.getenv("PYNETDICOM_AET")
PyNETDICOM_PORT = os.getenv("PYNETDICOM_PORT")

# SOP Classes used in Presentation Context
## Study Root Query/Retrieve Move
STUDY_ROOT_QR_MOVE = "1.2.840.10008.5.1.4.1.2.2.2"
## SOP Class UID
RT_IMAGE_CLASS_UID = "1.2.840.10008.5.1.4.1.1.481.1"


# Implement the handler for evt.EVT_C_STORE
def handle_store(event):
    """Handle a C-STORE request event."""
    ds = event.dataset
    ds.file_meta = event.file_meta

    # Save the dataset using the SOP Instance UID as the filename
    path_to_save = Path("/home/luis/FM/testing_DICOM_C-MOVE") / ds.SOPInstanceUID
    ds.save_as(path_to_save, enforce_file_format=True)

    # Return a 'Success' status
    return 0x0000

handlers = [(evt.EVT_C_STORE, handle_store)]


def main():
    print("Hello from Learning-Varian-Daemon-with-Python!")

    # Create an Application Entity
    ae = AE(PyNETDICOM_AET)  # AE Title
    ae.add_requested_context(STUDY_ROOT_QR_MOVE)  # C-MOVE
    ae.add_requested_context(RT_IMAGE_CLASS_UID)  # RT Image SOP Class

    # Define the presentation contexts for the Storage SCP
    contexts = [build_context(RT_IMAGE_CLASS_UID)]

    # Create an association with Varian DB
    assoc = ae.associate(
        addr = VarianDB_IP,
        port = int(VarianDB_PORT),
        ae_title = VarianDB_AET,
    )

    # Start our Storage SCP in non-blocking mode
    scp = ae.start_server(
        address=(PyNETDICOM_IP, int(PyNETDICOM_PORT)),
        block=False,
        evt_handlers=handlers,
        contexts=contexts,
    )