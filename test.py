import requests
import base64
import json
import os
import random
import cv2
import numpy as np
import urllib
import sys

flag = sys.argv[1]
base_path = os.getcwd()

def get_style(emotion):
    files = os.listdir(os.path.join("Styles/", emotion))
    file_num = random.randint(0, len(files)-1)
    print("Style Template pathname: ", os.path.join(os.path.join("Styles", emotion), files[file_num]))
    style_template = open(os.path.join(os.path.join("Styles", emotion), files[file_num]), 'rb')
    return style_template, os.path.join(os.path.join("Styles", emotion), files[file_num])

def stylize(content_image, style_template):
    url = "https://api.deepai.org/api/neural-style"
    response = requests.post(
                url,
                files={
                        'style': style_template,
                        'content': content_image,
                },
                headers={'api-key': '583e0dbc-44e0-460e-bf7e-972929020dfd'}
        )
    generated_image = open('generated_image.jpg','wb')
    print("response.json(): ", response.json())
    generated_image.write(requests.get(response.json()['output_url']).content)
    generated_image.close()

    return generated_image

def hackItUp():
    filename = "content_image.jpg"
    #encoded_string = base64.b64encode(image_file.read())
    cam = cv2.VideoCapture(0)

    cv2.namedWindow("test")

    img_counter = 0
    URL = "http://172.20.10.5:8080/shot.jpg"
    while True:
        # ret, frame = cam.read()
        # cv2.imshow("test", frame)
        # if not ret:
        #     break
        img_arr = np.array(bytearray(urllib.request.urlopen(URL).read()),dtype=np.uint8)
        img = cv2.imdecode(img_arr,-1)
        # cv2.imshow('IPWebcam',img)
        k = cv2.waitKey(1)

        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k%256 == 32:
            # SPACE pressed
            img_name = filename
            cv2.imwrite(img_name, img)
            print("{} written!".format(img_name))
            break

    cam.release()
    cv2.destroyAllWindows()
    
    emotion = "random"
    content_image = open(filename, "rb")
    if(flag == "true"):
        r = requests.post(
            'http://max-facial-emotion-classifier.max.us-south.containers.appdomain.cloud/model/predict',
            files={
                'image': content_image
            }
        )
        content_image.close()
        if(len(((json.loads(r.content))["predictions"])) > 0):
            emotion = (((((json.loads(r.content))["predictions"])[0])["emotion_predictions"])[0])["label"]

        print("#"*50, emotion, "#"*50)
    
    style_template, applied_style_file = get_style(emotion)

    content_image = open(filename, "rb")
    stylize(content_image, style_template)
    content_image.close()

    content_image = cv2.imread("content_image.jpg", 1)
    content_image = cv2.resize(content_image, (500, 500))
    cv2.imshow("Content_image", content_image)

    style_image = cv2.imread(applied_style_file, 1)
    style_image = cv2.resize(style_image, (500, 500))
    cv2.imshow("Style_image", style_image)


    generated_image = cv2.imread("generated_image.jpg", 1)
    generated_image = cv2.resize(generated_image, (500, 500))
    cv2.imshow("Generated_image", generated_image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    


hackItUp()