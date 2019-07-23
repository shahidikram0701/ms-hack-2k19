import requests
import base64

with open('./Examples/sadness/2.jpg', "rb") as image_file:
    # encoded_string = base64.b64encode(image_file.read())
    encoded_string = image_file
r = requests.post(
    "http://max-facial-emotion-classifier.max.us-south.containers.appdomain.cloud/model/predict",
    files={
        'image': open('./Examples/sadness/2.jpg', "rb")
    }
)

print(r.content)