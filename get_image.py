import os

from pynetdicom import AE, debug_logger, Association
from pynetdicom.sop_class import SOPClass
from pydicom.dataset import Dataset

from dotenv import load_dotenv

#debug_logger()
load_dotenv()  # This loads the variables from .env file
VarianDB_IP = os.getenv("VARIAN_DB_IP")
VarianDB_PORT = os.getenv("VARIAN_DB_PORT")
VarianDB_AET = os.getenv("VARIAN_DB_AET")

# Varian's Conformace Presentation Context
STUDY_ROOT_QR_FIND = "1.2.840.10008.5.1.4.1.2.2.1"

# Constant query's attributes (clinic specific)
PATIENT_ID = "11111"
STUDY_ID = "RapidArc QA Test"


def get_series_UID(
        patient_id: str,
        study_id: str,
        assoc: Association
        ) -> set[str]:
    
    # Create the identifier (query) dataset
    ds = Dataset()
    ds.QueryRetrieveLevel = "SERIES"
    ds.PatientID = patient_id
    ds.StudyID = study_id
    ds.SeriesInstanceUID = ""

    responses = assoc.send_c_find(ds, STUDY_ROOT_QR_FIND)
    series_UID = set()
    for (status, identifier) in responses:
        if '0xff00' == f"0x{status.Status:04x}":
            series_UID.add(identifier.SeriesInstanceUID)
        elif '0x0000' == f"0x{status.Status:04x}":
            print("Getting series UID done!")
        else:
            print("Connection timed out, was aborted or received invalid response")

    return series_UID


def get_images_UID(
        patient_id: str,
        study_id: str,
        series_UID: str,
        assoc: Association
        ) -> set[str]:

        # Create the identifier (query) dataset
        ds = Dataset()
        ds.QueryRetrieveLevel = "IMAGE"
        ds.PatientID = patient_id
        ds.StudyID = study_id
        ds.SeriesInstanceUID = series_UID
        ds.SOPInstanceUID = ""

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

        image_UIDs = set()
        try:
            series_uid = get_series_UID(PATIENT_ID, STUDY_ID, assoc)

            for serie_uid in series_uid:
                image_UIDs.update(get_images_UID(PATIENT_ID, STUDY_ID, serie_uid, assoc))
                
            print(f"Number of image UIDs: {len(image_UIDs)}")

        finally:
            assoc.release()
        
    else:
        print("Association rejected, aborted or never connected")



if __name__ == "__main__":
    main()