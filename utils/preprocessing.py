import io
from PIL import Image

def preprocess_image(image_bytes: bytes) -> Image.Image:
    """
    Prepares the input image bytes for the YOLO model.
    YOLO models accept PIL Images directly, so we just convert the bytes.
    """
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    return image
