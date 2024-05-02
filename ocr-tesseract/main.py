import io
import os
from hashlib import sha256

import cv2
import numpy as np
import pytesseract
from config import app_configs, settings
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pdf2image import convert_from_bytes
from PIL import Image
from services.redis import get_key, set_key_async
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(**app_configs)


async def process_image(image_data: bytes):
    image = Image.open(io.BytesIO(image_data))
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    gray = cv2.medianBlur(gray, 3)

    text = pytesseract.image_to_string(Image.fromarray(gray))

    return text


async def ocr_pdf(pdf_data: bytes):
    # Convert PDF to images
    images = convert_from_bytes(pdf_data)

    # Process each image using OCR
    ocr_text = ""
    for image in images:
        image_data = np.array(image)
        gray = cv2.cvtColor(image_data, cv2.COLOR_RGB2GRAY)
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        gray = cv2.medianBlur(gray, 3)
        text = pytesseract.image_to_string(Image.fromarray(gray))
        ocr_text += text + "\n"

    return ocr_text


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGINS_REGEX,
    allow_credentials=True,
    allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),
    allow_headers=settings.CORS_HEADERS,
)


@app.get("/ping", include_in_schema=False)
async def ping() -> dict[str, str]:
    return {
        "ping": "pong!",
    }


@app.post("/ocr/image/")
async def upload_file(file: UploadFile = File(...)):
    image_data = await file.read()

    image_hash = sha256(image_data).hexdigest()
    text = get_key(image_hash)
    if text:
        return JSONResponse(content={"text": text})

    text = await process_image(image_data)

    await set_key_async(image_hash, text)

    return JSONResponse(content={"text": text})


@app.post("/ocr/image/filepath")
async def process_file_path(file_path: str):
    if not os.path.isfile(file_path):
        return JSONResponse(content={"error": "File not found."}, status_code=404)

    with open(file_path, "rb") as file:
        image_data = file.read()

    image_hash = sha256(image_data).hexdigest()
    text = get_key(image_hash)
    if text:
        return JSONResponse(content={"text": text})

    text = await process_image(image_data)

    await set_key_async(image_hash, text)

    return JSONResponse(content={"text": text})


@app.post("/ocr/pdf/")
async def ocr_pdf_endpoint(file: UploadFile = File(...)):
    # Read the PDF file from the request
    pdf_data = await file.read()

    # Generate a hash of the PDF content
    pdf_hash = sha256(pdf_data).hexdigest()

    # Check if OCR text for this PDF is already cached
    cached_text = get_key(pdf_hash)
    if cached_text:
        return JSONResponse(content={"text": cached_text})

    # Perform OCR on the PDF
    ocr_text = await ocr_pdf(pdf_data)

    # Cache the OCR text
    await set_key_async(pdf_hash, ocr_text)

    return JSONResponse(content={"text": ocr_text})


@app.post("/ocr/pdf/filepath")
async def ocr_pdf_filepath(pdf_path: str):
    # Check if the file exists
    if not os.path.isfile(pdf_path):
        return JSONResponse(content={"error": "File not found."}, status_code=404)

    # Read the PDF file
    with open(pdf_path, "rb") as file:
        pdf_data = file.read()

    # Generate a hash of the PDF file path
    pdf_hash = sha256(pdf_data).hexdigest()

    # Check if OCR text for this PDF is already cached
    cached_text = get_key(pdf_hash)
    if cached_text:
        return JSONResponse(content={"text": cached_text})

    # Perform OCR on the PDF
    ocr_text = await ocr_pdf(pdf_data)

    # Cache the OCR text
    await set_key_async(pdf_hash, ocr_text)

    return JSONResponse(content={"text": ocr_text})
