from google.cloud import vision
import io

client = vision.ImageAnnotatorClient()


def run_vision_ocr(pil_image):

    client = vision.ImageAnnotatorClient()
    buffer = io.BytesIO()
    pil_image.save(buffer, format="PNG")
    content = buffer.getvalue()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    return texts[0].description if texts else ""
