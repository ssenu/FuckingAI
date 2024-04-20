from flask import Flask, render_template, request
import os
import testmodel as extract_text_from_image

app = Flask(__name__)

# 템플릿 디렉토리 설정
template_dir = os.path.abspath('templates')
app.template_folder = template_dir

# 이미지를 업로드할 디렉토리 설정
UPLOAD_FOLDER = 'C:/FuckingAI/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 메인 페이지 라우트
@app.route('/')
def main():
    return render_template('index.html')

# 이미지 업로드 및 텍스트 추출 라우트
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return '파일이 없습니다.'

    file = request.files['file']

    if file.filename == '':
        return '파일을 선택하세요.'

    if file:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        extracted_text = extract_text_from_image(file_path)
        return render_template('index.html', image_file=file_path, extracted_text=extracted_text)

if __name__ == '__main__':
    app.run(debug=True)
