from flask import Flask, jsonify, request, Response, session, render_template, redirect, url_for, make_response
import os
import requests
import json
import random
import base64

app = Flask(__name__)
app.secret_key = os.urandom(24) # for session

def get_emotion(content_image):
    url = 'http://max-facial-emotion-classifier.max.us-south.containers.appdomain.cloud/model/predict'
    response = requests.post(url, files=content_image)
    predictions = ((json.loads(response.content))["predictions"])[0]
    emotion = predictions["emotion_predictions"][0]["label"]
    
    return emotion

def get_style(emotion):
    files = os.listdir(os.path.join("./Styles/", emotion))
    file_num = random.randint(0, len(files)-1)
    style_template = open(os.path.join(os.path.join("./Styles", emotion), files[file_num]), 'rb')

    return style_template

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

def convert_and_save(b64_string):

    b64_string += '=' * (-len(b64_string) % 4)  # restore stripped '='s

    string = b'{b64_string}'

    with open("content_image.png", "wb") as fh:
        fh.write(base64.decodebytes(string))

@app.route('/nst')
def hello():
    return "Hello World" 

@app.route('/style_image', methods = ["POST"])
def style_image():
    if(request.method == "POST"):
        content_image = request.files
        print(content_image['image'])
        print(type(content_image['image']))
        return "ok"
        # with open("content_image.jpg", "wb") as fh:
        #     fh.write(base64.decodebytes(request.files['image']))
        
        # request.files['image'].save("content_image.jpg")
        # convert_and_save(request.files['image'].stream())

        # emotion = get_emotion({"image": open("content_image.png", 'rb')})

        # style_template = get_style(emotion)
        # generated_image = stylize(open("content_image.png", 'rb'), style_template)
        # return "OK"
        # return jsonify({
        #         'content_image': content_image,
        #         'style_template': style_template,
        #         'generated_image': generated_image
        # })
 

if __name__ == '__main__':
    app.run(host="0.0.0.0", port = 5001, debug = True, threaded = True)