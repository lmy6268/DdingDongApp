#실제로 크롤링동작하는 프로그램
from lxml.html import fromstring, tostring
import lxml.etree as etree
import datetime
# from multiprocessing import pool as p
import json  # json화
import requests
import time
import chulkyulCrawler as ch
weekDay = ['월', '화', '수', '목', '금', '토', '일']
KST = datetime.timezone(datetime.timedelta(hours=9))
today = datetime.datetime.today()
today = datetime.datetime(today.year, today.month, today.day, today.hour, today.minute, 0,
                          tzinfo=KST)
today = today.strftime('%Y-%m-%d %H:%M')
#초기데이터
# -> 사용자 정보(학번, 이름, 이메일, 아이디, 비밀번호) , 수업 정보

#이후에는 가지고 있는 정보를 토대로 알림을 수신.

def translateWord(date):
    query =f"translate({date}, '-', '')"
    query = f"translate({query},' ','')"
    date = f"translate({query},':','')"
    return date


# 과제 정보 크롤링 -> 학습활동 - 과제 (없는 경우도 있음 -> 예외처리 )
def crawlHomeWork(session, classList, className):
    url = classList[className]['link']
    html = session.get(url)
    parser = fromstring(html.text)
    assignCheck = parser.xpath(
        "//*[@id='coursemos-course-menu']/ul/li[2]/div/div[2]/ul/li/a[contains(text(),'과제')]")
    if (len(assignCheck) == 0):
        print("과제가 존재하지 않음")
    else:
        with session.get(assignCheck[0].get('href')) as assignSite:
            html = assignSite.content
            assignParser = fromstring(html)
            table = assignParser.xpath(
                "//*[contains(@class,'generaltable') and contains(@class,table-bordered)]/tbody")
            compareDateQuery = f"td[3][number({translateWord('text()')}) - number(translate(translate(translate('{today}', '-', ''),' ',''),':',''))<=1]"
            checkUnSubmitQuery = "td[4]='제출 완료'"
            assignList = table[0].xpath(f"//tr[{compareDateQuery} and {checkUnSubmitQuery}]")
            if assignList != []:
                for i in assignList:
                    aName = i[1].xpath("./a")[0].text
                    aDeadLine = i[2].text
                    aState = i[3].text
                    print(f"과제명: {aName} ,제출 마감: {aDeadLine} ,제출 상태:{aState}")
#수업 목록 크롤링 -> 사용자 정보에 등록용


def crawlClassList(parser):
    lists = {}
    t = parser.xpath("//ul[@class='my-course-lists coursemos-layout-0']")[
        0].xpath(".//div[@class='course-title']")
    link = parser.xpath(".//a[@class='course_link']")
    for i in range(len(t)):
        data = {}
        data["link"] = f"{link[i].attrib['href']}"
        timeString = f"{t[i].xpath('.//span')[0].text}"
        dataIdx = timeString.find('(')
        startTimeIdx = timeString.find('~')
        data["day"] = timeString[dataIdx+1]
        data["startTime"] = timeString[dataIdx+3:startTimeIdx]
        data["code"] = f"{link[i].attrib['href']}".split('=',1)[1]
        lists[f"{t[i].xpath('.//h3')[0].text}"] = data
    return lists


# 강의 수강 정보 크롤링 -> 기본 루프
def crawlVideo(session, parser):
    #강좌 리스트와 링크를 담는 사전(Dictionary)
    lessonList = {}
    #강좌 목록
    t = parser.xpath("//ul[@class='my-course-lists coursemos-layout-0']")
    #강좌 별 링크 -> 이걸 저장해 두어야 바로 즉각 대응이 가능 -> 로그인 시에 이 정보를 가져오도록 한다.!
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
    try:
        #강좌별 출석현황을 파악하기(병렬처리를 해도 됨)
        for k in lessonList:
            page = session.get(lessonList[f"{k}"])
            try:
                attendanceL = session.get(fromstring(page.text).xpath(
                    "//a[@title='Online-Attendance']")[0].attrib['href'])
            except IndexError:  # 발견하지 못한 경우
                attendanceL = session.get(fromstring(page.text).xpath(
                    "//a[@title='온라인출석부']")[0].attrib['href'])
            #출석부 테이블
            table = fromstring(attendanceL.text).xpath(
                "//table[@class='table  table-bordered user_progress_table']/tbody/tr/td")
            #레슨리스트 초기화
            lessonList[f"{k}"] = []
            now = [[i+1] for i in range(16)]  # 강의주차가 총 16주차이므로
            idx = 0
            final = ""
            cnt = 0  # 초기값세팅
            for i in table:  # 각 주차별 Loop
                if i.text != None and len(i.text) <= 2:  # 만약 강의가 있는 경우
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
                        cnt = 0
                        final = ""
                elif i.text == None:  # 과목명이 이미지 태그 내부에 있어서 None이라고 출력됨. 이 오류를 해결하기 위한 분기문
                    now[idx].append(i.text_content())  # 과목명 추출
                elif ":" in i.text:  # 각 영상 실행시간은 스킵
                    continue
                else:
                    now[idx].append(i.text)  # 영상 명과 수행 여부만 체크
            lessonList[f"{k}"] = now
        resD = json.dumps(lessonList, ensure_ascii=False)  # 결과물
        return resD

    except:
        print("생체인증 혹은 메일인증을 한 후 진행해 주세요.")
        return None  # 사용자가 메일 인증 또는 생체 인증을 해야하는 경우

#사용자 정보 가져오기


def crawlUserInfo(session):
    userData = {}
    main = session.get("https://cc.sungkyul.ac.kr")
    parser = fromstring(main.text)
    userPath = parser.xpath(
        "//*[@id='page-header']/nav/div/div[2]/ul/li[3]/div/ul[1]/li[1]/a")[0].get("href")
    userDataparser = fromstring(session.get(userPath).text)
    userData['stNID'] = userDataparser.xpath(
        "//*[@class='fitem  ']/div[@class = 'felement fstatic']")[0].text
    userData['stName'] = userDataparser.xpath(
        "//*[@id='page-header']/nav/div/div[2]/ul/li[2]")[0].text
    userData['stEmail'] = userDataparser.xpath(
        "//*[@id='id_email']")[0].get("value")
    userData['stDept'] = userDataparser.xpath(
        "//*[@id='id_department']")[0].get("value")
    return userData

#초기세팅 -> 로그인 시도


def login(fileName):
    with requests.session() as session:
        #실제 활용할 것
        # userID=f"{sys.argv[1]}" #받아온 사용자의 ID
        # userPW=f"{sys.argv[2]}" #받아온 사용자의 PW
        url = "https://cc.sungkyul.ac.kr/login/index.php"  # 성결대
        header = {
            'Referer': 'https://cc.sungkyul.ac.kr/login.php',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Mobile Safari/537.36'
        }
        f = open(fileName, 'r')
        account = f.readlines()
        userID = account[0].replace('\n', '')
        userPW = account[1]
        f.close()
        #유저데이터
        data = {
            'username': userID, 'password': userPW
        }
        session.post(url, headers=header, data=data)
        res = session.get("https://cc.sungkyul.ac.kr/")
        data = [userID, userPW, res.text]
        parser = fromstring(res.text)
        check = parser.xpath("//html[@class='html_login']")
        if check == []:
            try:
                href = parser.xpath(
                    ".//a[@class='course_link']")[0].attrib['href']
                session.get(href)
                return session
            except NameError or IndexError:
                return 0  # 사용자가 메일 인증 또는 생체 인증을 해야하는 경우
        else:
            return None  # 로그인이 안되는 경우


def mainLoop(fileName, type=0):
    start = time.time()
    try:
        session = login(fileName)
        if (session == None):
            raise ValueError  # 인증 필요
        elif session == 0:
            raise NameError  # 잘못된 정보
        html = session.get("https://cc.sungkyul.ac.kr/").text
        parser = fromstring(html)
        resD = crawlVideo(session, parser)
        userData = crawlUserInfo(session)
        userData["classList"] = crawlClassList(parser)
        for l in userData["classList"]:
            print(l)
            crawlHomeWork(session, userData["classList"], l)
    except ValueError:
        print("생체인증  혹은 메일인증을 한 후 진행해 주세요.")
    except NameError:
        print("일치하는 정보가 없습니다. 다시 시도해 주세요.")
    end = time.time()

    return userData


    # print("소요시간 : %f ms" % (end-start))
print(mainLoop("./crawl/test.txt"))
# print(weekDay[datetime.datetime.today().weekday()])
