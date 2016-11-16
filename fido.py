from bs4 import BeautifulSoup
import random
import bs4
import requests
import csv

def requests_get(url):
    USER_AGENTS = (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100 101 Firefox/22.0',
        'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0',
        ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.5 (KHTML, like Gecko) '
         'Chrome/19.0.1084.46 Safari/536.5'),
        ('Mozilla/5.0 (Windows; Windows NT 6.1) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46'
         'Safari/536.5')
    )
    try:
        r = requests.get(
            url,
            headers={'User-Agent': random.choice(USER_AGENTS)}
        )
    except ConnectionError:
        r.status_code = "Cinnection refused!"
    except requests.exceptions.ConnectionError:
        r.status_code = "Cinnection refused!"
    return r

def get_table(url,name_tag,class_attr):
    req = requests_get(url)
    req.encoding = 'utf-8'
    bsObj = BeautifulSoup(req.text,'lxml')
    tb = bsObj.find(name_tag,attrs={'class':class_attr})
    return tb


url = 'https://fidoalliance.org/certification/fido-certified/'
table_attr = "y-table-con fido-ready-page-con"
tb = get_table(url,'table',table_attr)
trs = tb.find_all('tr')
lines = []
for tr in trs:
    tds = list(filter(lambda x:isinstance(x,bs4.element.Tag),tr.contents))
    if len(tds) == 0:
        continue
    div = tds[0].div
    for span in filter(lambda x:isinstance(x,bs4.element.Tag),div.contents):
        #print(span.text)
        pass
    UAFClients = list(filter(lambda x:isinstance(x,bs4.element.Tag),div.contents))
    UAFServers = list(map(lambda span:'1' if isinstance(span.img,bs4.element.Tag) else '0',list(filter(lambda x:isinstance(x,bs4.element.Tag),tds[1].contents))))
    UAFAuthenticators = list(map(lambda span:'1' if isinstance(span.img,bs4.element.Tag) else '0',list(filter(lambda x:isinstance(x,bs4.element.Tag),tds[2].contents))))
    U2FAuthenticators = list(map(lambda span:'1' if isinstance(span.img,bs4.element.Tag) else '0',list(filter(lambda x:isinstance(x,bs4.element.Tag),tds[3].contents))))
    U2FServers = list(map(lambda span:'1' if isinstance(span.img,bs4.element.Tag) else '0',list(filter(lambda x:isinstance(x,bs4.element.Tag),tds[4].contents))))
    header = ['UAFClient','UAFServer','UAFAuthenticator','U2FServer','U2FAuthenticator']
    for i in range(len(UAFClients)):
        if UAFClients[i].text.isprintable() and len(UAFClients[i].text) and not UAFClients[i].text.isspace():
            line = (UAFClients[i].text,UAFServers[i],UAFAuthenticators[i],U2FAuthenticators[i],U2FServers[i])
            print(line)
            lines.append(line)

print(lines)
with open('fido.csv','w+') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)
    writer.writerows(lines)
