

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
