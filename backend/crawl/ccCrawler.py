#실제로 크롤링동작하는 프로그램
from lxml.html import fromstring, tostring
# from multiprocessing import pool as p
import json  # json화
import requests
import time
#생체인증 또는 이메일 인증 이슈가 있을 수 있겠다..
url = "https://cc.sungkyul.ac.kr/login/index.php"  # 성결대
session = requests.session()
header = {
    'Referer': 'https://cc.sungkyul.ac.kr/login.php',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Mobile Safari/537.36'
}
f = open("test.txt", 'r')
account = f.readlines()
userID = account[0]
userPW = account[1]
f.close()
#실제 활용할 것
# userID=f"{sys.argv[1]}" #받아온 사용자의 ID
# userPW=f"{sys.argv[2]}" #받아온 사용자의 PW

start = time.time()
#유저데이터
data = {
    'username': userID, 'password': userPW
}
#로그인 후 세션 유지하기
session = requests.session()
session.post(url, headers=header, data=data)
res = session.get("https://cc.sungkyul.ac.kr/")
html = res.text
parser = fromstring(html)
check = parser.xpath("//html[@class='html_login']")
#만약 로그인이 된다면
if check == []:
    #강좌 리스트와 링크를 담는 사전(Dictionary)
    lessonList = {}
    #강좌 목록
    t = parser.xpath("//ul[@class='my-course-lists coursemos-layout-0']")
    #강좌 별 링크
    link = parser.xpath(".//a[@class='course_link']")
    #강좌명
    t = t[0].xpath(".//div[@class='course-title']")

    #강좌 사전에 각각의 값을 넣음
    n = len(t)  # 수강하는 강좌의 수
    for i in range(n):
        lessonList[f"{t[i].xpath('.//h3')[0].text}"] = f"{link[i].attrib['href']}"
    # pool=p(processes=2)
    '''
    이후에 이메일 혹은 생체 인증을 위한 부분이 나온다. 
    만약 해당 부분이 안된 경우, 
    사용자에게 알릴 수 있어야 한다.
    '''
    try :
        #강좌별 출석현황을 파악하기(병렬처리를 해도 됨)
        for k in lessonList:
            page = session.get(lessonList[f"{k}"])
            attendanceL = session.get(fromstring(page.text).xpath(
                "//a[@title='온라인출석부']")[0].attrib['href'])
            #출석부 테이블
            table = fromstring(attendanceL.text).xpath(
                "//table[@class='table  table-bordered user_progress_table']/tbody/tr/td")
            #레슨리스트 초기화
            lessonList[f"{k}"] = []
            now = [[i+1] for i in range(16)]
            idx = 0; final = ""; cnt = 0
            for i in table:
                if i.text != None and len(i.text) <= 2:
                    if i.text == 'O' or i.text == 'X':
                        if cnt == 1:
                            final = i.text
                        else:
                            now[idx].append(i.text)
                            cnt += 1

                    elif i.text == '\xa0' or i.text == '-':
                        continue
                    else:
                        if len(now[idx]) > 2:
                            now[idx].append(f"result: {final}")
                        idx = int(i.text)-1
                        cnt = 0; final = ""
                elif i.text == None:  # 과목명이 이미지 태그 내부에 있어서 None이라고 출력됨. 이 오류를 해결하기 위한 분기문
                    now[idx].append(i.text_content())  # 과목명 추출
                elif ":" in i.text:  # 각 영상 실행시간은 스킵
                    continue
                else: now[idx].append(i.text)  # 영상 명과 수행 여부만 체크
            lessonList[f"{k}"] = now
            resD = json.dumps(lessonList, ensure_ascii=False)  # 결과물

    except :
        pass #사용자가 메일 인증 또는 생체 인증을 해야하는 경우


    

#로그인이 안되는 경우
else:
    resJson = {
        "message": "계정 정보가 잘못되었습니다. 다시 시도하여 주세요"
    }
    resD = json.dumps(resJson, ensure_ascii=False)  # 결과물
end = time.time()
# print(resD, "소요시간 : %f ms" % (end-start))
