import sys, requests
from bs4 import BeautifulSoup
import re
import datetime
import threading
import time
import requests
import win32api
import win32con
import win32gui

normalorigindata = set()
normaloriginlist = []
normalorigin = []

sworigindata = set()
sworiginlist = []
sworigin = []

bugcounter = 0

def init_notice():
    global normalorigindata, normaloriginlist, normalorigin, bugcounter
    bugcounter = 0
    normalorigindata = set()
    normalorigin = []
    normaloriginlist = []
    print("공지 초기화")
    normalurl = "https://newgh.gnu.ac.kr/cs/na/ntt/selectNttList.do?mi=6694&bbsId=2351"    
    normal = requests.get(normalurl)
    normalcroll = BeautifulSoup(normal.content, "lxml")
    normalnotice = normalcroll.select("a.nttInfoBtn")

    for i in range(len(normalnotice)):
        temptitle = re.sub("\t|\r|\n", "", normalnotice[i].text)
        templink = normalnotice[i].get("data-id")
        normaloriginlist.append({"href": templink, "title": temptitle})
        normalorigin.append(temptitle)
    normalorigindata = set(normalorigin)

def init_swnotice():
    global sworigin, sworiginlist, sworigindata, bugcounter
    bugcounter = 0
    sworigin = []
    sworiginlist = []
    sworigindata = set()
    print("SW공지 초기화")
    swurl = "https://newgh.gnu.ac.kr/cs/na/ntt/selectNttList.do?mi=6695&bbsId=2352"
    sw = requests.get(swurl)
    swcroll = BeautifulSoup(sw.content, "lxml")
    swnotice = swcroll.select("a.nttInfoBtn")
    
    for i in range(len(swnotice)):
        temptitle = re.sub("\t|\r|\n", "", swnotice[i].text)
        templink = swnotice[i].get("data-id")
        sworiginlist.append({"href": templink, "title": temptitle})
        sworigin.append(temptitle)
        
    sworigindata = set(sworigin)


def normalcheck_notice():
    global normalorigindata
    print("normalcheck")
    normalhref = "https://newgh.gnu.ac.kr/cs/na/ntt/selectNttInfo.do?mi=6694&bbsId=2351&nttSn="
    normalurl = "https://newgh.gnu.ac.kr/cs/na/ntt/selectNttList.do?mi=6694&bbsId=2351"
    normal = requests.get(normalurl)
    normalcroll = BeautifulSoup(normal.content, "lxml")

    tempnotice = normalcroll.select("a.nttInfoBtn")
    temp = []
    tempdata = set()
    templist = []

    for i in range(len(tempnotice)):
        temptitle = re.sub("\t|\r|\n", "", tempnotice[i].text)
        templink = tempnotice[i].get("data-id")
        temp.append(temptitle)
        templist.append({"href": templink, "title": temptitle})
    nmtemp = normalorigindata
    tempdata = set(temp)
    temp = tempdata - nmtemp
    if(len(tempdata) != len(nmtemp)):
        print("차이 발생")
        if(len(tempdata) > len(nmtemp)):
            count = tempdata - nmtemp
            for i in count:
                nmtemp = set(sworigin.append(""))

    if (len(temp) > 0):
        for i in temp:
            for index in range(len(templist)):
                if (bugcounter > 10):
                    return kakao_send_error(error="code error, need to check and excute again")
                if (i == templist[index].get("title")):
                    title = templist[index].get("title")+"\n"+ normalhref + templist[index].get("href")
                    bugcounter = bugcounter + 1
                    kakao_send_text(title)
                    print(i)
        init_notice()


def swcheck_notice():
    global sworigindata, sworigin, bugcounter
    print("swcheck")

    swurl = "https://newgh.gnu.ac.kr/cs/na/ntt/selectNttList.do?mi=6695&bbsId=2352"
    swhref = "https://newgh.gnu.ac.kr/cs/na/ntt/selectNttInfo.do?mi=6695&bbsId=2352&nttSn="
    sw = requests.get(swurl)
    swcroll = BeautifulSoup(sw.content, "lxml")

    tempnotice = swcroll.select("a.nttInfoBtn")
    temp = []
    tempdata = set()
    templist = []

    for i in range(len(tempnotice)):
        temptitle = re.sub("\t|\r|\n", "", tempnotice[i].text)
        templink = tempnotice[i].get("data-id")
        temp.append(temptitle)
        templist.append({"href": templink, "title": temptitle})
    swtemp = sworigindata
    tempdata = set(temp)
    temp = tempdata - swtemp
    if(len(tempdata) != len(swtemp)):
        print("차이 발생")
        if(len(tempdata) > len(swtemp)):
            count = tempdata - swtemp
            for i in count:
                swtemp = set(sworigin.append(""))

    if (len(temp) > 0):
        print(temp)
        for i in temp:
            for index in range(len(templist)):
                if (bugcounter > 10):
                    return kakao_send_error(error="code error, need to check and excute again")
                if (i == templist[index].get("title")):
                    title = templist[index].get("title")+"\n"+ swhref + templist[index].get("href")
                    bugcounter = bugcounter + 1
                    kakao_send_text(title)
                    print(i)
        init_swnotice()

def findPost(flag, newText, lateText): #놓친거 있을때 놓친거 제일 최신거와 제일 늦은거 입력 , 공백은 모두 지워서
    global normalorigin, sworigin, normaloriginlist, sworiginlst
    normaltemp = normalorigin
    swtemp = sworigin

    swhref = "https://newgh.gnu.ac.kr/cs/na/ntt/selectNttInfo.do?mi=6695&bbsId=2352&nttSn="
    normalhref = "https://newgh.gnu.ac.kr/cs/na/ntt/selectNttInfo.do?mi=6694&bbsId=2351&nttSn="

    newText = newText.replace(' ', '')
    lateText = lateText.replace(' ', '')

    for i in range(len(normaltemp)): #공백제거
        normaltemp[i] = normaltemp[i].replace(' ', '')

    for i in range(len(swtemp)):
        swtemp[i] = swtemp[i].replace(' ', '')

    if flag == 3 :
        starting_crolling()

    else:
        if (flag == 1):
            startAt = swtemp.index(newText)
            endAt = swtemp.index(lateText)

            for i in range(startAt, endAt+1):
                print(sworiginlist[i].get('title'))
                title = str(sworiginlist[i].get('title')) + swhref + str(sworiginlist[i].get('data-id'))
                kakao_send_text(title)

            starting_crolling()
                
        elif(flag == 0):
            startAt = normaltemp.index(newText)
            endAt = normaltemp.index(lateText)

            for i in range(startAt, endAt+1):
                print(normaloriginlist[i].get('title'))
                title = str(normaloriginlist[i].get('title')) + normalhref + str(normaloriginlist[i].get('data-id'))
                kakao_send_text(title)
            
            starting_crolling()

 

# 키보드 엔터 입력
def push_enter(hwnd):
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
    time.sleep(0.1)
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)


# 카카오 메세지 보내기
def kakao_send_text(text):
    # tester = ['관리자1', '관리자2', '관리자3', '관리자4']
    #captions = ['cs 1학년', 'cs 2학년', 'cs 3학년', 'cs 4학년', 'cs 외국인']
    #captions = ['구석방', '이가현조교님','이자룡조교님','박유리조교님']
    captions = ['황혁주']
    for caption in captions:
        hwnd_main = win32gui.FindWindow(None, caption)
        hwnd_edit = win32gui.FindWindowEx(hwnd_main, None, "RichEdit50W", None)
        win32api.SendMessage(hwnd_edit, win32con.WM_SETTEXT, 0, text)
        push_enter(hwnd_edit)
        time.sleep(0.1)


# 카카오 메세지 에러용
def kakao_send_error(error):
    #captions = ['황혁주', '전인혁', '성재석', '김학률']
    #captions = ['관리자1','관리자2','관리자3']
    captions = ['황혁주']
    for caption in captions:
        hwnd_main = win32gui.FindWindow(None, caption)
        hwnd_edit = win32gui.FindWindowEx(hwnd_main, None, "RichEdit50W", None)
        win32api.SendMessage(hwnd_edit, win32con.WM_SETTEXT, 0, error)
        push_enter(hwnd_edit)


def starting_crolling():
    normalcheck_notice()
    swcheck_notice()
    threading.Timer(30, starting_crolling).start()


if __name__ == "__main__":
    print(datetime.datetime.now().strftime('%c'), ': 구석봇v2.0 가동 시작')
    init_notice()
    init_swnotice()
    findPost(1, "학습동아리 프로그램 신청안내(~2021.09.10. 이룸시스템에 신청)", "『코딩역량강화 프로그램』전문가 초청 특강")

