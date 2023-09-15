#실제로 크롤링동작하는 프로그램
from lxml.html import fromstring
from datetime import datetime as dt
from datetime import timezone as tz
from datetime import timedelta as delta
# from multiprocessing import pool as p
import json  # json화
import requests
import sys
weekDay = ['월', '화', '수', '목', '금', '토', '일']
KST = tz(delta(hours=9))
today = dt.today()
today = dt(today.year, today.month, today.day, today.hour, today.minute, 0,
                          tzinfo=KST)
today= today.strftime('%Y%m%d%H%M')
todayFirstWeekDate=  (dt.today()- delta(days = dt.today().weekday())).strftime('%m월%0d일')
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
    hwList = []
    url = classList['link']
    html = session.get(url)
    parser = fromstring(html.text)
    assignCheck = parser.xpath(
        "//*[@id='coursemos-course-menu']/ul/li[2]/div/div[2]/ul/li/a[contains(text(),'과제')]")
    try:
        if (len(assignCheck) == 0):
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
                        hwList.append(f"{aName} , {aDeadLine}")
            return hwList

    except FileNotFoundError:
        return None
        
#수업 목록 크롤링 -> 사용자 정보에 등록용


def crawlClassList(parser):
    lists = []
    t = parser.xpath("//ul[@class='my-course-lists coursemos-layout-0']")[
        0].xpath(".//div[@class='course-title']")
    link = parser.xpath(".//a[@class='course_link']")
    for i in range(len(t)):
        data = {}
        data["name"] = f"{t[i].xpath('.//h3')[0].text}"
        data["link"] = f"{link[i].attrib['href']}"
        timeString = f"{t[i].xpath('.//span')[0].text}"
        dataIdx = timeString.find('(')
        startTimeIdx = timeString.find('~')
        data["day"] = timeString[dataIdx+1]
        data["startTime"] = timeString[dataIdx+3:startTimeIdx]
        data["code"] = f"{link[i].attrib['href']}".split('=',1)[1]
        lists.append(data)
    return lists


#온라인 출석 체크 (인자 - > session, 강의명, 기준일 )

# 오늘 날짜가 있는 주차에 출석하지 않은 영상이 있는 경우, 해당 강의 정보를 가져온다.
def crawlOnlineAtdc(session,lesson,stdDate=None):
    html = session.get(lesson['link']).text
    parser = fromstring(html)
    dayList=parser.xpath('//*[@id="region-main"]/div/div/div[4]/div/ul/li') 
    attList = parser.xpath('//*[@id="region-main"]/div/div/div[3]/div/ul/li[contains(@class,attendance_section)]')
    data =[]
    returnClassList = []
    for i in attList:
        data.extend([data for data in i.itertext() if not data.isdigit()]) #주차별로 출석, 결석 , - 데이터만 가져온다.(인덱스 -> 주차)
    for i in range(len(dayList)): #
        weekName =dayList[i].attrib['aria-label']
        firstWeekDate =weekName.split('[')[1].split('-')[0] 
        if data[i] == '결석' and firstWeekDate == todayFirstWeekDate:  #만약 이번 주차 수업이 결석으로 체크되어있다면
            vdList =dayList[i].xpath("./div[@class='content']/ul/li[contains(@class,modtype_vod)]//div[@class='activityinstance']//span[@class='instancename']")
            for vid in vdList:
                returnClassList.append(vid.text)


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
        url = "https://cc.sungkyul.ac.kr/login/index.php"  # 성결대
        header = {
            'Referer': 'https://cc.sungkyul.ac.kr/login.php',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Mobile Safari/537.36'
        }
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
                html = fromstring(session.get(href).text)
                if html.xpath('//form[@action = "/local/ruauth/"]')==[]:
                    return session
                else :
                    raise NameError
            except NameError or IndexError:
                return 0  # 사용자가 메일 인증 또는 생체 인증을 해야하는 경우
        else:
            return None  # 로그인이 안되는 경우(회원 정보 업데이트 필요) -> DB에 있는 경우, 사용자에게 알림을 보냄



def main(id,pw,tp,classList=None):
    try:
        session = login(id,pw)
        if (session == None):
            raise NameError  # 잘못된 정보
        elif session == 0:
            raise ValueError  # 인증이 필요함
        #base 
        html = session.get("https://cc.sungkyul.ac.kr/").text
        parser = fromstring(html)
        #return by type
        if tp == '1': #사용자 정보 반환 
            userData = crawlUserInfo(id,pw)
            userData["classList"] = crawlClassList(parser)
            print(json.dumps(userData,ensure_ascii=False))
        elif tp == '2': #과제 현황
            hwList = {}
            for i in classList:
                hwCheck = crawlHomeWork(session,i,i['name'])
                if not(hwCheck ==None or hwCheck == []):
                    hwList[i['name']] = hwCheck
            if(len(hwList)>0):
                print(json.dumps(hwList,ensure_ascii=False))
            else:
                print("None")
        elif tp == '3': #영상 강의 현황
            crawlOnlineAtdc(session,classList[0])
    #handle Error
    except ValueError:
        print("ValueError")
    except NameError:
        print("NameError")

if __name__=='__main__':
    id,pw = sys.argv[1],sys.argv[2]
    tp = sys.argv[3]
    if(len(sys.argv)>4) : #강의 목록을 보낸경우
        classList = eval(sys.argv[4])
        # print(classList,type(classList))
        main(id,pw,tp,classList)
    else:
        main(id,pw,tp)
    # main(id,pw,'0')
