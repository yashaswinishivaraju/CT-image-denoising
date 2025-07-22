//this will generate dummy example.dcmfile,wich can be used for flask web app
//If you want a real DICOM CT scan, download from:CBIS-DDSM (breast cancer),The Cancer Imaging Archive,Kaggle DICOM datasets

import numpy as np
import pydicom
from pydicom.dataset import Dataset, FileDataset
import datetime
import os

def create_dummy_dicom(save_path="sample_data/example.dcm"):
    # Create a 256x256 grayscale image with synthetic pattern
    image = np.zeros((256, 256), dtype=np.uint16)
    cv = 1000
    for i in range(256):
        for j in range(256):
            image[i, j] = cv + ((i * j) % 300)

    # File meta information
    file_meta = pydicom.Dataset()
    file_meta.MediaStorageSOPClassUID = pydicom.uid.SecondaryCaptureImageStorage
    file_meta.MediaStorageSOPInstanceUID = pydicom.uid.generate_uid()
    file_meta.ImplementationClassUID = pydicom.uid.PYDICOM_IMPLEMENTATION_UID

    # Dataset
    ds = FileDataset(save_path, {}, file_meta=file_meta, preamble=b"\0" * 128)
    ds.Modality = "CT"
    ds.ContentDate = datetime.date.today().strftime('%Y%m%d')
    ds.ContentTime = datetime.datetime.now().strftime('%H%M%S')
    ds.PatientName = "Test^CTPatient"
    ds.PatientID = "123456"
    ds.Rows, ds.Columns = image.shape
    ds.SamplesPerPixel = 1
    ds.PhotometricInterpretation = "MONOCHROME2"
    ds.BitsAllocated = 16
    ds.BitsStored = 16
    ds.HighBit = 15
    ds.PixelRepresentation = 1
    ds.PixelData = image.tobytes()

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    ds.save_as(save_path)
    print(f"Saved dummy DICOM file at: {save_path}")

if __name__ == "__main__":
    create_dummy_dicom()
