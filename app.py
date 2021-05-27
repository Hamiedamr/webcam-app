from flask import json, request
from flask import Flask
import base64
import cv2
import numpy as np
from blind_features import EmotionRecognition,GenderRecognition,AgeDetector

async_mode = None
app = Flask(__name__)
emotions = EmotionRecognition()
genders = GenderRecognition()
ages = AgeDetector()


def data_uri_to_cv2_img(uri):
    encoded_data = uri.split(',')[1]
    nparr = np.fromstring(base64.decodebytes(encoded_data.encode()), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

@app.route('/', methods=['GET'])
def home():
    return '<h1>Hello</h1>'
@app.route('/', methods=['POST'])
def parse_request():
    errors = {}
    success = False
    file = ""
    out_emotion = ""
    out_gender = ""
    out_age = ""
    if 'data' not in request.form['data']: 
        return json.dumps({'message': 'No file part in the request'},400,{'ContentType':'application/json'})
    else:
        file = data_uri_to_cv2_img(request.form['data'])
    if len(file) and request.form['f'] == 'emotion':
        # _,__,out_emotion = emotions.detect(file)
        # success = True
        # if success and len(out_emotion) > 0:
            # return json.dumps({'message':out_emotion[0]})
        pass
    if len(file) and request.form['f'] == 'gender':
        _,_,out_gender = genders.detect(file)
        success = True
        if success and len(out_gender) > 0:
            return json.dumps({'message':out_gender[0]})
    if len(file) and request.form['f'] == 'age':
        _,_,out_age=ages.detect(file)
        success = True
        if success and len(out_age) > 0:
            return json.dumps({'message':str(out_age[0])})
    if success and errors:
        return  json.dumps({'errors':'File(s) successfully uploaded'})
    else:
        return json.dumps({'errors':'Error!','status_code':400,'ContentType':'application/json'})

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)