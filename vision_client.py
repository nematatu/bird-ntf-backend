from google.cloud import vision
from PIL import Image
import io

client = vision.ImageAnnotatorClient()


def run_vision_ocr(image_path):
    print("take OCR..")
    with Image.open(image_path) as img:
        byte_arr = io.BytesIO()
        img.save(byte_arr, format="PNG")
        content = byte_arr.getvalue()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    return texts[0].description.strip() if texts else ""
