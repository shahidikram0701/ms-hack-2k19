
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, jsonify, request
import os
import requests
import json
import random
import base64
import shutil

app = Flask(__name__)

base_path = '/home/shahidikram0701/mysite/'


def get_full_path(path):
    return os.path.join(base_path, path)

def get_emotion(content_image):
    print("Content Image: ", content_image)
    url = 'http://max-facial-emotion-classifier.max.us-south.containers.appdomain.cloud/model/predict'
    response = requests.post(url, files=content_image)
    print("RESPONSE - ",response.content)
    while(1):
        predictions = ((json.loads(response.content))["predictions"])
        if len(predictions) != 0:
            break
    print(len(predictions), predictions)
    predictions = predictions[0]
    emotion = predictions["emotion_predictions"][0]["label"]

    return emotion

def get_style(emotion):
    files = os.listdir(os.path.join(base_path+"Styles/", emotion))
    file_num = random.randint(0, len(files)-1)
    print("Style Template pathname: ", os.path.join(os.path.join(base_path+"Styles", emotion), files[file_num]))
    style_template = open(os.path.join(os.path.join(base_path+"Styles", emotion), files[file_num]), 'rb')
    return (style_template, os.path.join(os.path.join(base_path+"Styles", emotion), files[file_num]), file_num+1)

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

# def convert_and_save(imgstring):
#     imgdata = base64.decodestring(image_64_encode)
#     filename = 'content_image.png'  # I assume you have a way of picking unique filenames
#     with open(filename, 'wb') as f:
#         f.write(imgdata)
#     # fTemp = Image.open(filename)
#     # fTemp.save("content_image_new.jpg")
#     # print("ERROR SOLVE:", type(fTemp), fTemp.size)
#     #fsmall = fTemp.resize((16,30),Image.ANTIALIAS)
#     #fsmall.save(filename)

@app.route('/test')
def hello():
    print("*********************TEST*********************")
    return jsonify("Hello World")

@app.route('/style_image_with_emotion', methods = ["POST"])
def style_image_with_emotion():
    if(request.method == "POST"):
        content = json.loads(request.data)
        print("_"*10, content.keys(), "_"*10)
        content_image = content['image']
        emotion = content['emotion']
        print("_"*10, emotion)
        if emotion == "":
            emotion = "neutral"
        print("_"*10, emotion)


        def save(filename):
            # print("_"*10, type(content_image), "_"*10)
            image_64_decode = base64.decodebytes(content_image.encode())
            image_result = open(filename, 'wb')
            image_result.write(image_64_decode)

            image_result.close()

        save('content_image.jpg')

        style_template, style_file_path, num = get_style(emotion)
        generated_image = stylize(open("content_image.jpg", 'rb'), style_template)

        shutil.copy("content_image.jpg", "/home/shahidikram0701/mysite/static/")
        shutil.copy("generated_image.jpg", "/home/shahidikram0701/mysite/static/")
        shutil.copy(style_file_path, "/home/shahidikram0701/mysite/static/")

        os.rename("/home/shahidikram0701/mysite/static/"+ style_file_path.split('/')[-1], "/home/shahidikram0701/mysite/static/style.jpg")

        return jsonify("Success")


@app.route('/style_image', methods = ["POST"])
def style_image():
    if(request.method == "POST"):
        content_image = json.loads(request.data)
        print("-START-"*50)
        print("Content Image: ", type(content_image), content_image.keys(), type(content_image['image']))
        print("-END-"*50)

        def save(filename):
            image_64_decode = base64.decodebytes(content_image['image'].encode())
            image_result = open(filename, 'wb')
            image_result.write(image_64_decode)

            image_result.close()
        save('content_image.jpg')
        save('content_image2.jpg')
        #optimize_image.save('content_image.jpg', quality=99, optimize=True)
        # convert_and_save(content_image['image'])


        # content_image['image'].save("content_image.jpg")

        # emotion = get_emotion({"image": open("content_image.jpg", 'rb')})

        image_result = open('content_image.jpg', 'rb')
        emotions = ["happiness", "sadness", "anger", "fear", "surprise", "contempt", "disgust", "neutral"]
        e = random.randint(0, len(emotions)-1)
        emotion = emotions[e] #get_emotion({"image": image_result})
        image_result.close()



        # print("EMOTION: ", emotion)
        style_template = get_style(emotion)
        generated_image = stylize(open("content_image2.jpg", 'rb'), style_template)
        return jsonify(emotion)
        # return jsonify("OK")

        # return jsonify({
        #         'content_image': content_image,
        #         'style_template': style_template,
        #         'generated_image': generated_image
        # })
