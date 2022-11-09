#Load Library
from lxml.html import fromstring, tostring
import json  # json화
import requests
import time

url = "https://smart.sungkyul.ac.kr/atdc/" #성결대 전자출결 시스템 주소
header = {
  'Referer':   "https://smart.sungkyul.ac.kr/atdc",
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Mobile Safari/537.36'
}
userID = input("학번을 입력하세요")
userPW = input("비밀번호를 입력하세요")
#유저데이터
data = {
    'admin_id': userID, 'admin_pw': userPW
}
with requests.session() as session:
    #로그인을 먼저 해야함. -> 저장되어 있던 데이터를 이용하여 로그인 진행.
    session.post(url,headers=header,data=data)
    res = session.get("https://smart.sungkyul.ac.kr/atdc/mid_main")
    html = res.text
    parser = fromstring(html)
    print(parser)
    #로그인 한 후, 전자출결 탭으로 이동 

    #원하는 과목으로 탭을 전환

    #지정 날짜의 출석여부를 확인

    #서버에 결과값으로 전달


