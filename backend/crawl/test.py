string = "[컴퓨터공학과/002] (금 14:40~15:30, 16:30~17:20)"
#여기서 추려낼 내용 -> 요일 / 시작 시간
dataIdx = string.find('(')
startTimeIdx = string.find('~')
print(string[dataIdx+1], string[dataIdx+3:startTimeIdx])