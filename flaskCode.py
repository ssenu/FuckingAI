from flask import Flask, request
from datetime import datetime
import loadModelCode
import os

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def handle_request():
    if 'image' in request.files:

        if not os.path.exists('image'):
            os.makedirs('image')
        
        imagefile = request.files['image']
        filename = datetime.today().strftime("%Y%m%d%H%M%S") + '.jpg'
        image_path = os.path.join('image', filename)
        imagefile.save(image_path)

        text = loadModelCode.imageFunc("image/"+filename)
        print("테스트ㅡㅡ")
        returntext = text 
        return returntext

    else:
        return "오류남"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
