import re
import urllib.request as j
import sqlite3
from bs4 import BeautifulSoup
import urllib.parse as l



def getcatalog(key):

    key = l.urlencode({'q0':key})
    url = 'http://opac.ncu.edu.cn/opac/search_adv_result.php?sType0=any&'+key+'&logic1=AND&sType1=any&q1=&pageSize=20&sort=score&desc=on&with_ebook=on%27'

    res = j.urlopen(url)
    soup = BeautifulSoup(res,'html.parser',from_encoding='utf-8')
    catalog = soup.select('tr')

    n = 0
    content=[]
    for x in catalog:
        if n ==0:
            n=n+1
            continue

        q = re.findall('FFF">(.*?)</td>',str(x))

        title = re.findall('blank">(.*?)</a>',q[1])[0]
        href = 'http://opac.ncu.edu.cn/opac/item.php?' + re.findall('href="(.*?)">',q[1])[0].split('"')[0]

        zuozhe = q[2]
        cb = q[3]
        ssh = q[4]
        lx = q[5]

        if cb.split()==[]:
            cbxx = ['无', '无']

        else:
            cbxx=cb.split()

        cbs=cbxx[0]
        cbrq = cbxx[1]
        content.append({'xh':str(n),'href':href,"book_name":title,"publish_date":cbrq,"writter":zuozhe,"publisher":cbs})
        n=n+1
    return content



