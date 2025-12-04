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

# Create our Identifier (query) dataset
ds = Dataset()
ds.PatientName = "QC^IMRT"
ds.QueryRetrieveLevel = "STUDY"
ds.StudyInstanceUID = ""
ds.StudyDate = ""
ds.StudyID = ""

# Varian's Conformace Presentation Context
STUDY_ROOT_QR_FIND = "1.2.840.10008.5.1.4.1.2.2.1"

def main():
    print("Hello from learning-daemon-py!")

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

        responses = assoc.send_c_find(ds, STUDY_ROOT_QR_FIND)
        for (status, identifier) in responses:
            if status:
                # Show status with hexadecimal representation
                print(f"C-Find query status: 0x{status.Status:04x}")
                print(identifier)
            else:
                print("Connection timed out, was aborted or received invalid response")
            #break
        assoc.release()

    else:
        print("Association rejected, aborted or never connected")



if __name__ == "__main__":
    main()