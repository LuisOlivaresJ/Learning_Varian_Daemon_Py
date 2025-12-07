import os

from pynetdicom import AE, debug_logger, Association
from pynetdicom.sop_class import SOPClass
from pydicom.dataset import Dataset

from dotenv import load_dotenv

#debug_logger()

# Load environment variables (AE Title, IP, Port)
load_dotenv()  # This loads the variables from .env file
VarianDB_PORT = os.getenv("VARIAN_DB_PORT")
VarianDB_AET = os.getenv("VARIAN_DB_AET")
VarianDB_IP = os.getenv("VARIAN_DB_IP")


# Varian's Conformace Presentation Context
STUDY_ROOT_QR_FIND = "1.2.840.10008.5.1.4.1.2.2.1"

# Constant query's attributes (clinic specific)
PATIENT_ID = "11111"
STUDY_ID = "RapidArc QA Test"  # This corresponds to the Course Name in Eclipse


def get_series_UIDs(
        patient_id: str,
        study_id: str,
        assoc: Association
        ) -> set[str]:
    """Helper function to get all Series Instance UIDs for a given patient and study."""
    
    # Create the identifier (query) dataset
    ds = Dataset()
    ds.QueryRetrieveLevel = "SERIES"
    ds.PatientID = patient_id
    ds.StudyID = study_id
    ds.SeriesInstanceUID = ""

    # Send the C-FIND request
    responses = assoc.send_c_find(ds, STUDY_ROOT_QR_FIND)
    series_UID = set()  # To hold unique series UIDs
    for (status, identifier) in responses:
        if '0xff00' == f"0x{status.Status:04x}":
            series_UID.add(identifier.SeriesInstanceUID)
        elif '0x0000' == f"0x{status.Status:04x}":
            pass
        else:
            print("Connection timed out, was aborted or received invalid response")

    return series_UID


def get_image_UIDs(
        patient_id: str,
        study_id: str,
        serie_UID: str,
        assoc: Association
        ) -> set[str]:
        """Helper function to get all Image SOP Instance UIDs for a given patient, study and serie."""

        # Create the identifier (query) dataset
        ds = Dataset()
        ds.QueryRetrieveLevel = "IMAGE"
        ds.PatientID = patient_id
        ds.StudyID = study_id
        ds.SeriesInstanceUID = serie_UID
        ds.SOPInstanceUID = ""

        # Send the C-FIND request
        responses = assoc.send_c_find(ds, STUDY_ROOT_QR_FIND)
        image_UID = set()
        for (status, identifier) in responses:
            if '0xff00' == f"0x{status.Status:04x}":
                #print(identifier.SOPInstanceUID)
                image_UID.add(identifier.SOPInstanceUID)
            elif '0x0000' == f"0x{status.Status:04x}":
                pass
                #print("Getting series UID done!")
            else:
                print("Connection timed out, was aborted or received invalid response")

        return image_UID


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

        image_UIDs = set()  # To hold all image unique Image UIDs
        try:
            series_uid = get_series_UIDs(PATIENT_ID, STUDY_ID, assoc)

            for serie_uid in series_uid:
                image_UIDs.update(get_image_UIDs(PATIENT_ID, STUDY_ID, serie_uid, assoc))
                
            print(f"Number of image UIDs: {len(image_UIDs)}")

        finally:  # Ensure the association is released
            assoc.release()
        
    else:
        print("Association rejected, aborted or never connected")



if __name__ == "__main__":
    main()