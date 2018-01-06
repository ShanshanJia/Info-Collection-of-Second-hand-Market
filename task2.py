#! /usr/bin/python
# task2.py - Parse html, extract and filter data from scrapped web pages with
# Beautiful Soup and Requests

import requests
from bs4 import BeautifulSoup

url = 'http://bbs.skykiwi.com/forum.php'
header = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
baseTable = []
extendTable = []

for i in range(9, 10):
    payload = {'mod': 'forumdisplay', 'fid': '17', 'page': str(i)}
    page = requests.get(url, params=payload, headers=header)
    soup = BeautifulSoup(page.text, "lxml")
    tbodyList = soup.select("tbody[id*=normalthread_]")
    for tbody in tbodyList:
        if tbody.select("span[title*=20]"):
            postTime = tbody.select("span[title*=20]")
            postDate = postTime[0]['title'].split()
            posts = tbody.select('a[class="xst"]')
            postTitle = posts[0].string
            postLink = 'http://bbs.skykiwi.com/' + posts[0]['href']
            baseTable.append([postTitle, postLink, postDate[0]])
        else:
            tbody.decompose()
print(len(baseTable))

for i in range(len(baseTable)):
    bodyPage = requests.get(baseTable[i][1], headers=header)
    soup = BeautifulSoup(bodyPage.text, "lxml")
    postInfo = soup.find(class_='pstatus')
    if postInfo:
        postInfo.decompose()
    tdList = soup.select('td[class="t_f"]')
    bodyText = tdList[0].get_text()
    extendTable.append([baseTable[i][0], baseTable[i][1], baseTable[i][2], bodyText])
print(len(extendTable))


def hitKeywords(tList):
    keyList = ['内存', 'IPHONE', '懒人床上小桌子']
    result = False
    for key in keyList:
        if (key in tList[0]) or (key in tList[3]):
            result = True
            break
    return result


filterTable = filter(hitKeywords, extendTable)
text = ['Here are some posts you might be interested in:']
for post in filterTable:
    text.append(post[0] + ', ' + post[1] + ', ' + post[2])
fullText = '\n'.join(text)
print(fullText)
