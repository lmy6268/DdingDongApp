#실제로 크롤링동작하는 프로그램
from lxml.html import fromstring
import datetime
# from multiprocessing import pool as p
import json  # json화
import requests
import sys
weekDay = ['월', '화', '수', '목', '금', '토', '일']
KST = datetime.timezone(datetime.timedelta(hours=9))
today = datetime.datetime.today()
today = datetime.datetime(today.year, today.month, today.day, today.hour, today.minute, 0,
                          tzinfo=KST)
today = today.strftime('%Y%m%d%H%M')
#초기데이터
# -> 사용자 정보(학번, 이름, 이메일, 아이디, 비밀번호) , 수업 정보

#이후에는 가지고 있는 정보를 토대로 알림을 수신.
def daydiff(day):
    if day == 5 :
        return 52359
    elif day == 3:
        return 32359



# 과제 정보 크롤링 -> 학습활동 - 과제 (없는 경우도 있음 -> 예외처리 )
def crawlHomeWork(session, classList, className):
    needToSubmit = {}
    url = classList[className]['link']
    html = session.get(url)
    parser = fromstring(html.text)
    assignCheck = parser.xpath(
        "//*[@id='coursemos-course-menu']/ul/li[2]/div/div[2]/ul/li/a[contains(text(),'과제')]")
    try:
        if (len(assignCheck) == 0):
            print("과제가 존재하지 않음")
            raise FileNotFoundError
        else:
            with session.get(assignCheck[0].get('href')) as assignSite:
                html = assignSite.content
                assignParser = fromstring(html)
                #현재 시간과 마감시간의 차이
                timeCheck =f"td[3][number(translate(translate(translate(text(),'-',''),' ',''),':',''))-{today} >=0 and number(translate(translate(translate(text(),'-',''),' ',''),':',''))-{today} <={daydiff(3)} ]"
                submitCheck = f"td[4]='미제출'"
                query = f"//*[contains(@class,'generaltable') and contains(@class,table-bordered)]/tbody/tr[{timeCheck} and {submitCheck}]"
                assignList = assignParser.xpath(query)
                if assignList != []:
                    for i in assignList:
                        aName = i[1].xpath("./a")[0].text
                        aDeadLine = i[2].text
                        aState = i[3].text
                        needToSubmit['과제명']
                        print(f"과제명: {aName} ,제출 마감: {aDeadLine} ,제출 상태:{aState}")
    except FileNotFoundError:
        return json.dumps({"data":None})
        
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


#온라인 출석 체크 (인자 - > session, 강의명, 기준일 )
def crawlOnlineAtdc(session,lesson,stdDate=None):
    html = session.get(lesson['link']).content
    parser = fromstring(html)
    dayList=parser.xpath('//*[@id="region-main"]/div/div/div[4]/div/ul/li')
    attList = parser.xpath('//*[@id="region-main"]/div/div/div[3]/div/ul/li[contains(@class,attendance_section)]')
    data =[]
    for i in attList:
        data.extend([data for data in i.itertext() if not data.isdigit()])
    for i in range(len(dayList)):
        if not (data[i] == '-'):
            weekName =dayList[i].attrib['aria-label']
            vdList =dayList[i].xpath("./div[@class='content']/ul/li[contains(@class,modtype_vod)]//div[@class='activityinstance']//span[@class='instancename']")
            for i in vdList:
                print(i.text)


#사용자 정보 가져오기
def crawlUserInfo(id,pw):
    session = login(id,pw)
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


def login(userID,userPW):
    with requests.session() as session:
        #실제 활용할 것
        # userID=f"{sys.argv[1]}" #받아온 사용자의 ID
        # userPW=f"{sys.argv[2]}" #받아온 사용자의 PW
        url = "https://cc.sungkyul.ac.kr/login/index.php"  # 성결대
        header = {
            'Referer': 'https://cc.sungkyul.ac.kr/login.php',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Mobile Safari/537.36'
        }
        # f = open(fileName, 'r')
        # account = f.readlines()
        # userID = account[0].replace('\n', '')
        # userPW = account[1]
        # f.close()

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
            return None  # 로그인이 안되는 경우(회원 정보 업데이트 필요) -> DB에 있는 경우, 사용자에게 알림을 보냄


def mainLoop(id,pw):
    try:
        session = login(id,pw)
        if (session == None):
            raise NameError  # 인증 필요
        elif session == 0:
            raise ValueError  # 잘못된 정보
        html = session.get("https://cc.sungkyul.ac.kr/").text
        parser = fromstring(html)
        # resD = crawlVideo(session, parser)
        userData = crawlUserInfo(id,pw)
        userData["classList"] = crawlClassList(parser)
        crawlOnlineAtdc(session,userData['classList']['논리회로'])
        return userData
    except ValueError:
        # print("생체인증  혹은 메일인증을 한 후 진행해 주세요.")
        print("ValueError")
    except NameError:
        print("일치하는 정보가 없습니다. 다시 시도해 주세요.")
        print("NameError")

if __name__=='__main__':
    # print(mainLoop("./crawl/test.txt"))
    mainLoop(sys.argv[0],sys.argv[1])
