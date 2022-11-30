#Load Library
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
import time
from datetime import datetime

url = "https://smart.sungkyul.ac.kr" #성결대 전자출결 시스템 주소
mainUrl ="https://smart.sungkyul.ac.kr/atdc/atdc"
header = {
  'Referer':   "https://smart.sungkyul.ac.kr",
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Mobile Safari/537.36'
}

def initDriver():
  #만약 드라이버가 없다면 자동으로 설치해줌
  options = webdriver.ChromeOptions()
  options.add_argument('headless')
  options.add_argument('window-size=1920x1080')
  options.add_argument("disable-gpu")
  driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),chrome_options=options)
  return driver

#로그인을 진행하는 함수 
def login(userData):
    userID = userData["stcID"]
    userPW = userData["stcPW"]
    driver = initDriver()
    driver.get(mainUrl)
    driver.delete_all_cookies() #초기화
    driver.implicitly_wait(0.1)
    driver.find_element(By.XPATH,"//*[@id='admin_id']").send_keys(userID)
    driver.find_element(By.XPATH,"//*[@id='admin_pw']").send_keys(userPW)
    driver.find_element(By.XPATH,"//*[@id='action']").click()
    time.sleep(0.1)
    driver.get(mainUrl)
    time.sleep(0.01)
    return driver

#사용자 정보와 과목명을 입력으로 받음 -> 출석여부 확인
def mainLoop(userData,subject,date=None):
    if date == None:
      today =datetime.today().strftime("%Y.%m.%d")
    else:
      today = date
    with login(userData) as driver:
      #로그인이 될 때까지 시도
      tryCnt = 0
      while(1):
        try:
          driver.find_element(By.XPATH,f"//*[@id='sjco']/option[contains(text(),'{subject}')]").click()
          break
        except NoSuchElementException:
          tryCnt+=1
          print("로그인 실패")
          #5번동안 시도해봄.
          if tryCnt == 5:
            print("멈춤")
            return #이때는 사용자 정보 변경을 의심해보아야 하거나 학교 전자출결 시스템에 오류가 생긴 것.
          driver = login(userData)
      driver.implicitly_wait(0.01)
      table =driver.find_element(By.XPATH,"//*[@id='form_list']/div[2]/table")
      #현재 날짜를 이용하여, 해당 날의 출석 여부를 확인 
      try:
        isChecked = table.find_elements(By.XPATH,f"//tr[td//text()[contains(., '{today}')]]/td")[3].text
        if isChecked == '/':
          isChecked = False
        else:
          isChecked = True
        return isChecked
      except IndexError:
        print("해당 일자에는 수업이 존재하지 않습니다.")
        # exit()

#메인 함수
if __name__ =="__main__":
  start = time.time()
  userData={"stcID": "20170993","stcPW":"lmky7168@@"}
  if mainLoop(userData,"C프로그래밍"):
    print("정상 출석입니다.")
  else:
    print("결석입니다.")
  end = time.time()
  print("소요시간 : ",end-start,"ms")
