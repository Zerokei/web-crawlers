import requests # 获取网页
# import queue
from bs4 import BeautifulSoup
from lxml import etree

Set = set()

def Get(faurl,url):
    if (url[0:4] == "http") or (url[0] == "/"):
        return
    
    url = faurl+url

    if url in Set:
        return
    Set.add(url)

    datalist = []
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'lxml')

    file = open('+'.join(url.split("/")[2:]), 'w', encoding='utf-8')
    file.write(soup.get_text(separator=" "))
    file.close()

    print('Download...'+url)
    print('+'.join(url.split("/")[2:]))    
    pos = url.rfind('/')
    myurl = url[0:pos+1]
    for a in soup.find_all('a'):
        if(str(a).count('href') == 0):
            continue        
        nexturl = a['href']
        Get(myurl, nexturl)



baseurl = 'http://shakespeare.mit.edu/'

html = requests.get(baseurl)
soup = BeautifulSoup(html.text, 'lxml')
for a in soup.find_all('a'):
    Get(baseurl, a['href'])


#https://www.zhihu.com/question/20899988/answer/2014832208
#https://blog.csdn.net/Waspvae/article/details/80738559
#https://blog.csdn.net/qq_28404829/article/details/100181480
