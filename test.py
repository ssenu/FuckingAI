import os
import urllib.request
import json
import ssl
import requests

ssl._create_default_https_context = ssl._create_unverified_context


client_id = "m5BZvGwGFdxBz7kXd00K"
client_secret = "LSPvwNzShK"

keyword = input("검색어 입력 : ")
end = int(input("다운받을 사진 수 : "))
start = 1 # 검색시작 위치
display = 10 # 한 번에 표시할 검색 결과 개수 (기본 10, 최대값 100)
n = 1

# 폴더 경로 설정
folder_path = f"C:/FuckingAI/images/{keyword}"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

for i in range(start, end, display):
    url = f"https://openapi.naver.com/v1/search/image?query={keyword}&display={display}&start={i}"
    Headers = {"X-Naver-Client-Id": client_id,
               "X-Naver-Client-Secret": client_secret}
    request = requests.get(url, headers=Headers)
    python_obj = json.loads(request.text)
    items = python_obj['items']

    for j in range(len(items)):
        img_url = items[j]['link']
        img_file = requests.get(img_url, verify=False)
        file_path = os.path.join(folder_path, f'{n}.jpg')

        with open(file_path, 'wb') as f:
            f.write(img_file.content)
            print(f'{n}번째 사진 다운로드..')
            n += 1
