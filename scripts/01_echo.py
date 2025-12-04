"""
01_echo.py
This script implements a C-ECHO request to verify connectivity with the Varian Daemon.
"""


import os

from pynetdicom import AE, debug_logger
from pydicom.dataset import Dataset

from dotenv import load_dotenv

debug_logger()  # Enable debugging logs for pynetdicom

load_dotenv()  # This loads the variables from .env file
VarianDB_IP = os.getenv("VARIAN_DB_IP")
VarianDB_PORT = os.getenv("VARIAN_DB_PORT")
VarianDB_AET = os.getenv("VARIAN_DB_AET")

# Varian Conformace Presentation Context
VERIFICATION_CONTEXT = "1.2.840.10008.1.1"


def main():
    print("Hello from Learning-Varian-Daemon-with-Python!")

    # Create an Application Entity
    ae = AE("FM_SCU")  # User AE Title
    ae.add_requested_context(VERIFICATION_CONTEXT)

    # Create an association with Varian DB
    assoc = ae.associate(
        addr = VarianDB_IP,
        port = int(VarianDB_PORT),
        ae_title = VarianDB_AET
    )

    if assoc.is_established:
        print("Association established!")

        try:
            status = assoc.send_c_echo()
        finally:  # Ensure the association is released, even if C-ECHO fails
            assoc.release()
    else:
        print("Failed to associate")


if __name__ == "__main__":
    main()
