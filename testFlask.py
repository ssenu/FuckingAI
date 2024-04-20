from flask import Flask, request
from datetime import datetime
import testmodel
import torch
import torchvision
import torchvision.transforms as transforms
from PIL import Image
import torchvision.models as models
import torch.nn as nn
import torchvision.transforms as T
import os

app = Flask(__name__)

@app.route('/', methods=['POST'])
def handle_request():
    if 'image' in request.files:
    # 'image' 폴더가 없는 경우 생성
        if not os.path.exists('image'):
            os.makedirs('image')
        
        imagefile = request.files['image']
        filename = datetime.today().strftime("%Y%m%d%H%M%S") + '.jpg'
        image_path = os.path.join('image', filename)
        imagefile.save(image_path)
        # 여기에 이미지 처리 및 모델 적용 등을 수행한다.
        text = testmodel.imageFunc("image/"+filename)
        print("테스트ㅡㅡ")
        return text

    else:
        return "No image received"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
