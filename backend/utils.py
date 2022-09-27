import base64
import io
from PIL.Image import Image

def resizeAndEncodeImage(image: Image):
    width, height = image.size
    if width > height:
        height = height / width * 640
        width = 640
    else:
        width = width / height * 640
        height = 640
    image = image.resize((int(width), int(height)))

    file = io.BytesIO()
    image.save(file, format="JPEG")
    encoded = base64.b64encode(file.getvalue()).decode('ascii')
    return encoded