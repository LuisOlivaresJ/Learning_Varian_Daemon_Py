import os
from pathlib import Path

from pynetdicom import AE, debug_logger, Association, evt, build_context

from pydicom.dataset import Dataset

from dotenv import load_dotenv


#debug_logger()


# Load environment variables (AE Title, IP, Port)
load_dotenv()  # This loads the variables from .env file
VarianDB_PORT = os.getenv("VARIAN_DB_PORT")
VarianDB_AET = os.getenv("VARIAN_DB_AET")
VarianDB_IP = os.getenv("VARIAN_DB_IP")

PyNETDICOM_IP = os.getenv("PYNETDICOM_IP")
PyNETDICOM_AET = os.getenv("PYNETDICOM_AET")
PyNETDICOM_PORT = os.getenv("PYNETDICOM_PORT")

SCP_AET = os.getenv("PyNetDICOM_SCP_IP_AET")


# SOP Classes used in Presentation Context
## Study Root Query/Retrieve Find
STUDY_ROOT_QR_FIND = "1.2.840.10008.5.1.4.1.2.2.1"
## Study Root Query/Retrieve Move
STUDY_ROOT_QR_MOVE = "1.2.840.10008.5.1.4.1.2.2.2"
## SOP Class UID
RT_IMAGE_CLASS_UID = "1.2.840.10008.5.1.4.1.1.481.1"


# Constant query's attributes (clinic specific)
PATIENT_ID = "11111"
STUDY_ID = "RapidArc QA Test"  # This corresponds to the Course Name in Eclipse


def get_series_UIDs(
        patient_id: str,
        study_id: str,
        assoc: Association,
        ) -> set[str]:
    """
    Helper function to get all Series Instance UIDs for a given patient and study.

    Returns:
        set[str]: A set of Series Instance UIDs.
    """
    
    # Create the identifier (query) dataset
    ds = Dataset()
    ds.QueryRetrieveLevel = "SERIES"
    ds.PatientID = patient_id
    ds.StudyID = study_id

    # We are interested only in RT Images
    ds.Modality = "RTIMAGE"

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
        date: str,
        assoc: Association
        ) -> set[str]:
        """
        Helper function to get all Image SOP Instance UIDs for a given patient, study and serie.

        Args:
            patient_id (str): The patient ID.
            study_id (str): The study ID.
            serie_UID (str): The series instance UID.
            date (str): The date to query. Should be a valid matching format according to DICOM standards 
                (e.g., "20250102-" for dates starting on 2025 January 02). See DICOM Standard PS3.4 Section Attribute Matching for details.

        Returns:
            set[str]: A set of Image SOP Instance UIDs.
        """

        # Create the identifier (query) dataset
        ds = Dataset()
        ds.QueryRetrieveLevel = "IMAGE"
        ds.PatientID = patient_id
        ds.StudyID = study_id
        ds.SeriesInstanceUID = serie_UID
        ds.SOPClassUID = ""
        ds.SOPInstanceUID = ""
        ds.ContentDate = date  # Query dates starting on 2025 January 01

        # Send the C-FIND request
        responses = assoc.send_c_find(ds, STUDY_ROOT_QR_FIND)
        image_UIDs = set()
        for (status, identifier) in responses:
            if '0xff00' == f"0x{status.Status:04x}":
                # If RT_Image, store the SOP Instance UID
                if identifier.SOPClassUID == RT_IMAGE_CLASS_UID:
                    print(f"ContentDate: {identifier.ContentDate}")
                    image_UIDs.add(identifier.SOPInstanceUID)
            elif '0x0000' == f"0x{status.Status:04x}":
                pass
                #print("Getting series UID done!")
            else:
                print("Connection timed out, was aborted or received invalid response")

        return image_UIDs



def main():
    print("Hello from Learning-Varian-Daemon-with-Python!")

    # Create an Application Entity
    ae = AE(PyNETDICOM_AET)  # AE Title
    ae.add_requested_context(STUDY_ROOT_QR_FIND)  # C-FIND
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


    if assoc.is_established:
        print("Association established!")

        #image_UIDs = set()  # To hold all image unique Image UIDs
        try:
            # FIND
            serie_uids = get_series_UIDs(PATIENT_ID, STUDY_ID, assoc)

            """ for serie_uid in serie_uids:
                image_UIDs.update(get_image_UIDs(PATIENT_ID, STUDY_ID, serie_uid, "20251101-", assoc))
                break  # Uncomment to process only first series
                
            print(f"Number of image UIDs: {len(image_UIDs)}") """

            # MOVE
            for serie_uid in serie_uids:

                # Create dataset and send the C-MOVE request
                ds = Dataset()
                ds.QueryRetrieveLevel = "SERIES"
                ds.PatientID = PATIENT_ID
                ds.StudyID = STUDY_ID
                ds.SeriesInstanceUID = serie_uid
                ds.ContentDate = "20251120"  # Create the request only for images taken on 2025 November 20

                if assoc.is_established:
                    print(f"Requesting C-MOVE for SeriesInstanceUID: {serie_uid}")
                    responses = assoc.send_c_move(
                        ds,
                        SCP_AET,  # Our storage service class provider (see 03_scp.py)
                        STUDY_ROOT_QR_MOVE
                    )
                    for (status, identifier) in responses:
                        if status:
                            print(f"C-MOVE response status: 0x{status.Status:04x}")
                        else:
                            print("Connection timed out, was aborted or received invalid response")

        finally:  # Ensure the association is released
            assoc.release()
        
    else:
        print("Association rejected, aborted or never connected")


if __name__ == "__main__":
    main()