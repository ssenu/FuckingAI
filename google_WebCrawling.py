from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import urllib.request
import os

serchName = input("검색어 입력 : ")
countnum = int(input("이미지 저장할 횟수 : "))

save_directory = f"./{serchName}"

if not os.path.exists(save_directory):
    os.makedirs(save_directory)



chrome_options = Options()
service = Service(executable_path=ChromeDriverManager().install())

# 브라우저 꺼짐 방지
chrome_options.add_experimental_option("detach", True)

# 불필요한 에러 메시지 없애기
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

#크롬 드라이버 설정
driver = webdriver.Chrome(service=service, options=chrome_options)

# 웹페이지 해당 주소 이동
driver.get("https://www.google.co.kr/imghp?hl=ko&tab=ri&authuser=0&ogbl")

elem = driver.find_element(By.CLASS_NAME, "gLFyf")
elem.send_keys(serchName)
elem.send_keys(Keys.RETURN)

# 많은 이미지를 구하기 위해 스크롤 내리기
SCROLL_PAUSE_TIME = 1

# 스크롤 높이 재기
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
   # 스크롤 아래로 내리기
   driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
   # 새로운 페이지가 load되기를 기다리기
   time.sleep(SCROLL_PAUSE_TIME)
   # 새로운 스크롤 높이 구하여 이전 스크롤 높이와 비교하기
   new_height = driver.execute_script("return document.body.scrollHeight")
   if new_height == last_height:
       try:
           driver.find_element(By.CSS_SELECTOR, ".mye4qd").click()
       except:
           break
   last_height = new_height


image_path = '//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div/div[3]/div[1]/a/img[1]'
countError = 0
# 이미지를 클릭하여 해당 이미지를 다운로드하기
images = driver.find_elements(By.CLASS_NAME, "rg_i.Q4LuWd")
count = 1
for image in images[:countnum]:
    try:
        image.click()
        time.sleep(2)
        imgUrl_element = driver.find_element(By.XPATH, image_path)
        imgUrl = imgUrl_element.get_attribute("src")
        if imgUrl:
            # 이미지를 다운로드하고 경로 설정된 디렉토리에 저장
            urllib.request.urlretrieve(imgUrl, os.path.join(save_directory, str(count) + ".jpg"))
            count += 1
    except Exception as e:
        print(f"Error occurred while downloading image {count}: {e}")
        countError += 1
driver.close()


print(f"검색어 : {serchName}")
print(f"시도한 횟수 : {countnum}")
print(f"실패 횟수 : {countError}")
print(f"저장된 이미지 수 : {countnum - countError}")