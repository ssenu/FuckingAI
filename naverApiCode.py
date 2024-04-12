import os
import urllib.request
import json
import ssl
import requests
import time

ssl._create_default_https_context = ssl._create_unverified_context()

client_id = "m5BZvGwGFdxBz7kXd00K"
client_secret = "LSPvwNzShK"

keywordList = ["사과", "배", "포도", "수박", "귤", "토마토", "망고", "자몽", "딸기", "파인애플", "키위", "복숭아", "바나나", "멜론", "참외", "체리", "레몬"]
print(keywordList[1])


for z in range(len(keywordList)):
    keyword = keywordList[z]
    end = 300
    start = 1  # 검색시작 위치
    display = 10  # 한 번에 표시할 검색 결과 개수 (기본 10, 최대값 100)
    n = 1

    # 폴더 경로 설정
    folder_path = f"./images/{keyword}"
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
            try:
                img_file = requests.get(img_url)
                img_file.raise_for_status()  # 이 부분 추가
            except requests.exceptions.HTTPError as err:
                print(f"HTTP 에러가 발생했습니다: {err}")
                continue
            except requests.exceptions.RequestException as err:
                print(f"요청 중 에러가 발생했습니다: {err}")
                continue

            # 파일 이름 설정
            file_extension = img_url.split('.')[-1].split('?')[0]
            file_name = f'{n}.{file_extension}'
            file_path = os.path.join(folder_path, file_name)

            # 파일 저장
            # time.sleep(1)
            try:
                with open(file_path, 'wb') as f:
                    try:
                        f.write(img_file.content)
                        print(f'{n}번째 사진 다운로드..')
                    except Exception as e:
                        print(f"{n}번째 사진 다운로드 에러..")
            except Exception as e:
                print(f"{n}번째 사진 저장 오류")
            finally:
                n += 1
