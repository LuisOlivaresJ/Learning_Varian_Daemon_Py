"""
A script to perform a C-FIND query to show how to request for specific DICOM tags.

Reference:
Eclipse 18.1 DICOM Conformance Statement
    Table 4-12: Study Root Request Identifier for Interactive Client Q/R C-FIND SCU
Pynetdicom Find Service Class User (SCU) Example
    https://pydicom.github.io/pynetdicom/stable/examples/qr_find.html
"""

import os

from pynetdicom import AE, debug_logger
from pynetdicom.sop_class import SOPClass
from pydicom.dataset import Dataset

from dotenv import load_dotenv
#debug_logger()

load_dotenv()  # This loads the variables from .env file
VarianDB_IP = os.getenv("VARIAN_DB_IP")
VarianDB_PORT = os.getenv("VARIAN_DB_PORT")
VarianDB_AET = os.getenv("VARIAN_DB_AET")

# Create our Identifier (query) dataset. In this case, we will query for all studies
# instancesUID that mathch Patient's Name "QC^IMRT"
ds = Dataset()
ds.PatientName = "QC^IMRT"
ds.QueryRetrieveLevel = "STUDY"
ds.StudyInstanceUID = ""
ds.StudyDate = ""
ds.StudyID = ""

# Varian's Conformace Presentation Context
STUDY_ROOT_QR_FIND = "1.2.840.10008.5.1.4.1.2.2.1"

def main():
    print("Hello from Learning-Varian-Daemon-with-Python!")

    # Create an Application Entity
    ae = AE("FM_SCU")  # User AE Title
    ae.add_requested_context(STUDY_ROOT_QR_FIND)

    # Create an association with Varian DB
    assoc = ae.associate(
        addr = VarianDB_IP,
        port = int(VarianDB_PORT),
        ae_title = VarianDB_AET
    )

    if assoc.is_established:
        print("Association established!")

        try:
            responses = assoc.send_c_find(ds, STUDY_ROOT_QR_FIND)
            for (status, identifier) in responses:
                if status:
                    # Show status with hexadecimal representation
                    print(f"C-Find query status: 0x{status.Status:04x}")
                    # Show the requested dateset tags
                    print(identifier)

                else:
                    print("Connection timed out, was aborted or received invalid response")
                #break

        finally:  # Ensure the association is released, even if C-FIND fails
            assoc.release()

    else:
        print("Association rejected, aborted or never connected")


if __name__ == "__main__":
    main()