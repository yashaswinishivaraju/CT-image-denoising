CT image Diagnosing (Offline DICOM Denoiser)

This project allows hospitals to upload DICOM (CT scan) images and applies denoising using **Wavelet Transform** and **Median Filtering** to improve image quality by ~15%.

a.Features
- Upload `.dcm` files
- Image enhancement using image processing techniques
- Fully offline and browser-based
- Python + Flask

b.To Run
-bash
pip install -r requirements.txt
cd app
python main.py
