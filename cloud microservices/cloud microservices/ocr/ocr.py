import os,io
from google.cloud import vision

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "google-config.json"
Folder_path = "ocr.jpg"

client = vision.ImageAnnotatorClient()

def validateImage():
    output = []
    with io.open(Folder_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # Performs label detection on the image file
    response = client.text_detection(image=image)
    texts = response.text_annotations
    # print(texts)
    for text in texts:
        print(text.description)
        output.append(text.description)
        return output



