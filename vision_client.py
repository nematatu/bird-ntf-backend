from google.cloud import vision
import io
from datetime import datetime

client = vision.ImageAnnotatorClient()


def run_vision_ocr(pil_image):

    client = vision.ImageAnnotatorClient()
    buffer = io.BytesIO()
    pil_image.save(buffer, format="PNG")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"images/test_{timestamp}.png"
    pil_image.save(filename)
    print(f"[保存完了] OCR用画像: {filename}")

    content = buffer.getvalue()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    return texts[0].description if texts else ""
