from flask import Flask, request, jsonify
import sys, requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

normalurl = "https://newgh.gnu.ac.kr/cs/na/ntt/selectNttList.do?mi=6694&bbsId=2351"
swurl = "https://newgh.gnu.ac.kr/cs/na/ntt/selectNttList.do?mi=6695&bbsId=2352"
normalhref = "https://newgh.gnu.ac.kr/cs/na/ntt/selectNttInfo.do?mi=6694&bbsId=2351&nttSn="
swhref = "https://newgh.gnu.ac.kr/cs/na/ntt/selectNttInfo.do?mi=6695&bbsId=2352&nttSn="

counts = 0
swcounts = 0
normalnotice = {}
swnotice = {}


def crolling_notice():
    global normalnotice
    normal = requests.get(normalurl)
    normalcroll = BeautifulSoup(normal.content, "lxml")
    normalnotice = normalcroll.select("a.nttInfoBtn")


def counting_normalnotice():
    global counts
    normaltemp = 0
    couns = 0
    normal = requests.get(normalurl)
    normalcroll = BeautifulSoup(normal.content, "lxml")
    normalNoticeNumber = normalcroll.select("td.BD_tm_none")
    for z in normalNoticeNumber:
        normalpoint = z.text
        if ("공지" != normalpoint):
            if (int(normaltemp) < int(normalpoint)):
                normaltemp = normalpoint

    for z in normalNoticeNumber:
        normalpoint = z.text
        if ("공지" != normalpoint):
            counts = couns
            print(counts)
            break
        couns = couns + 1


def crolling_swnotice():
    global swnotice
    sw = requests.get(swurl)
    swcroll = BeautifulSoup(sw.content, "lxml")
    swnotice = swcroll.select("a.nttInfoBtn")


def counting_swnotice():
    global swcounts
    swtemp = 0
    couns = 0
    sw = requests.get(swurl)
    swcroll = BeautifulSoup(sw.content, "lxml")
    swNoticeNumber = swcroll.select("td.BD_tm_none")
    for z in swNoticeNumber:
        swpoint = z.text
        if ("공지" != swpoint):
            if (int(swtemp) < int(swpoint)):
                swtemp = swpoint

    for z in swNoticeNumber:
        swpoint = z.text
        if ("공지" != swpoint):
            swcounts = couns
            print(swcounts)
            break
        couns = couns + 1


@app.route('/message', methods=['POST'])
def Message():
    global normalnotice, counts
    counting_normalnotice()
    crolling_notice()

    dataSend = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "listCard": {
                        "header": {
                            "title": "경상대학교 컴퓨터과학과 공지사항"
                        },
                        "items": [
                            {
                                "title": re.sub("\t|\r|\n", "", normalnotice[counts + 0].text),
                                "link": {
                                    "web": normalhref + normalnotice[counts + 0].get("data-id")
                                }
                            },
                            {
                                "title": re.sub("\t|\r|\n", "", normalnotice[counts + 1].text),
                                "link": {
                                    "web": normalhref + normalnotice[counts + 1].get("data-id")
                                }
                            },
                            {
                                "title": re.sub("\t|\r|\n", "", normalnotice[counts + 2].text),
                                "link": {
                                    "web": normalhref + normalnotice[counts + 2].get("data-id")
                                }
                            },
                            {
                                "title": re.sub("\t|\r|\n", "", normalnotice[counts + 3].text),
                                "link": {
                                    "web": normalhref + normalnotice[counts + 3].get("data-id")
                                }
                            }
                        ],
                        "buttons": [
                            {
                                "label": "공지사항보기",
                                "action": "webLink",
                                "webLinkUrl": "https://newgh.gnu.ac.kr/cs/na/ntt/selectNttList.do?mi=6694&bbsId=2351"
                            }
                        ]
                    }
                }
            ]
        }
    }
    return jsonify(dataSend)


@app.route('/swmessage', methods=['POST'])
def swMessage():
    global swnotice, swcounts
    counting_swnotice()
    crolling_swnotice()

    dataSend = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "listCard": {
                        "header": {
                            "title": "경상대학교 컴퓨터과학과 SW공지사항"
                        },
                        "items": [
                            {
                                "title": re.sub("\t|\r|\n", "", swnotice[swcounts + 0].text),
                                "link": {
                                    "web": swhref + swnotice[swcounts + 0].get("data-id")
                                }
                            },
                            {
                                "title": re.sub("\t|\r|\n", "", swnotice[swcounts + 1].text),
                                "link": {
                                    "web": swhref + swnotice[swcounts + 1].get("data-id")
                                }
                            },
                            {
                                "title": re.sub("\t|\r|\n", "", swnotice[swcounts + 2].text),
                                "link": {
                                    "web": swhref + swnotice[swcounts + 2].get("data-id")
                                }
                            },
                            {
                                "title": re.sub("\t|\r|\n", "", swnotice[swcounts + 3].text),
                                "link": {
                                    "web": swhref + swnotice[swcounts + 3].get("data-id")
                                }
                            }
                        ],
                        "buttons": [
                            {
                                "label": "공지사항보기",
                                "action": "webLink",
                                "webLinkUrl": "https://newgh.gnu.ac.kr/cs/na/ntt/selectNttList.do?mi=6694&bbsId=2351"
                            }
                        ]
                    }
                }
            ]
        }
    }
    return jsonify(dataSend)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True)
