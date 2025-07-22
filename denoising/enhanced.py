import pydicom
import numpy as np
import cv2
import pywt
import os
from scipy.ndimage import median_filter

def wavelet_denoise(image):
    coeffs = pywt.wavedec2(image, 'db1', level=2)
    coeffs_filtered = [coeffs[0]] + [
        tuple(pywt.threshold(subband, value=20, mode='soft') for subband in detail)
        for detail in coeffs[1:]
    ]
    denoised = pywt.waverec2(coeffs_filtered, 'db1')
    return np.clip(denoised, 0, 255).astype(np.uint8)

def anisotropic_diffusion(img, n_iter=10, kappa=50, gamma=0.1):
    img = img.astype(np.float32)
    for i in range(n_iter):
        # gradients
        deltaN = np.roll(img, -1, axis=0) - img
        deltaS = np.roll(img, 1, axis=0) - img
        deltaE = np.roll(img, -1, axis=1) - img
        deltaW = np.roll(img, 1, axis=1) - img

        # conduction
        cN = np.exp(-(deltaN / kappa) ** 2)
        cS = np.exp(-(deltaS / kappa) ** 2)
        cE = np.exp(-(deltaE / kappa) ** 2)
        cW = np.exp(-(deltaW / kappa) ** 2)

        # update
        img += gamma * (cN * deltaN + cS * deltaS + cE * deltaE + cW * deltaW)

    return np.clip(img, 0, 255).astype(np.uint8)

def enhance_image(input_path, output_path):
    # Load and normalize DICOM
    dicom_data = pydicom.dcmread(input_path)
    image = dicom_data.pixel_array.astype(np.float32)
    image -= np.min(image)
    image /= np.max(image)
    image *= 255
    image = image.astype(np.uint8)

    # Step 1: Wavelet Denoising
    wavelet_img = wavelet_denoise(image)

    # Step 2: Median Filter (3x3)
    median_img = median_filter(wavelet_img, size=3)

    # Step 3: Non-local Means Denoising (preserves texture)
    nlm_img = cv2.fastNlMeansDenoising(median_img, None, h=10, templateWindowSize=7, searchWindowSize=21)

    # Step 4: Anisotropic Diffusion
    diffused_img = anisotropic_diffusion(nlm_img, n_iter=8, kappa=30, gamma=0.15)

    # Step 5: Contrast Boost (15%)
    final_img = cv2.convertScaleAbs(diffused_img, alpha=1.15, beta=0)

    # Save
    cv2.imwrite(output_path, final_img)
