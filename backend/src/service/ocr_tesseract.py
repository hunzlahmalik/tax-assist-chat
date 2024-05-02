import requests
from django.conf import settings

OCR_API_BASE_URL = settings.OCR_API_BASE_URL


def ocr_image(image_path):
    url = f"{OCR_API_BASE_URL}/ocr/image/filepath"
    files = {"file": open(image_path, "rb")}
    response = requests.post(url, files=files)
    if response.status_code == 200:
        return response.json()["text"]
    else:
        return None


def ocr_pdf(pdf_path):
    url = f"{OCR_API_BASE_URL}/ocr/pdf/filepath"
    files = {"pdf_path": open(pdf_path, "rb")}
    response = requests.post(url, files=files)
    if response.status_code == 200:
        return response.json()["text"]
    else:
        return None


def ocr_pdf_from_bytes(pdf_bytes):
    url = f"{OCR_API_BASE_URL}/ocr/pdf/"
    files = {"file": ("pdf_file.pdf", pdf_bytes)}
    response = requests.post(url, files=files)
    if response.status_code == 200:
        return response.json()["text"]
    else:
        return None


def ocr_image_from_bytes(image_bytes):
    url = f"{OCR_API_BASE_URL}/ocr/image/"
    files = {"file": ("image_file.jpg", image_bytes)}
    response = requests.post(url, files=files)
    if response.status_code == 200:
        return response.json()["text"]
    else:
        return None
