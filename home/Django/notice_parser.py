import requests
import datetime
import json
from pymongo.mongo_client import MongoClient
from bs4 import BeautifulSoup
client = MongoClient('222.239.90.78', 30001)

db=client.chat_bot
notice = db.notice

def notice_crawler():
    notice_list=['http://sejong.korea.ac.kr/user/boardList.do?handle=102914&siteId=kr&id=kr_050108010000','http://sejong.korea.ac.kr/user/boardList.do?handle=101685&siteId=kr&id=kr_050108020000','http://sejong.korea.ac.kr/campuslife/notice/college','http://sejong.korea.ac.kr/user/boardList.do?handle=61751&siteId=kr&id=kr_050107000000','http://sejong.korea.ac.kr/campuslife/notice/scholarship','http://sejong.korea.ac.kr/campuslife/notice/career']
    DB_list =['corona_prevent', 'corona_action', 'common', 'event', 'scholarship', 'career']
    ul = open('/home/Django/update_log.txt', 'a')
#    temp=[]
    for k in range(len(notice_list)):
        now = datetime.datetime.now()
        req = requests.get(notice_list[k])
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        
        data1= soup.find('ul',{'class' : 'board_contents'})
        data2 = data1.findAll('p',{'class':'title'})
        data3 = data1.findAll('dd')
        data4 = data1.findAll('a')
        
        t = []
        l = []
        d =[]
        
        for i in range(len(data2)):
            j= 1+(i*3)
            t.append(data2[i].text.strip())
            data3[j] = str(data3[j])[4:14]
#            d.append(data3[j])
            d.append(datetime.datetime.strptime(data3[j],'%Y-%m-%d'))
            l.append("http://sejong.korea.ac.kr" + str(data4[i]).split('"')[1].replace("amp;",''))  
        t.reverse()
        l.reverse()
        d.reverse()        

#        for i in range(len(t)):
#            notice.insert({"category" : DB_list[k] , "title": t[i], "link" : l[i], "date" : d[i]})

#        for i in range(len(t)):
#           temp.append({"category" : DB_list[k] , "title": t[i], "link" : l[i], "date" : d[i]})
#        with open("notice.json", "w") as json_file:       
#            json.dump(temp, json_file)

        temp = notice.find({"category" : DB_list[k]},{"date" : True})
        cnt = temp.count()
        lastest_date = temp[cnt-1]["date"]
        temp = notice.find({"date" : lastest_date},{"title" : True, "date" : True, "_id" :False})
        
        lastest_title =[]
        for i in temp:
            lastest_title.append(i["title"])
        
        insert_list = []
        
        for i in range(len(d)):
            if d[i] > lastest_date:
                insert_list.append(i)
            elif d[i] < lastest_date:
                pass
            else:
                if t[i] in lastest_title:
                    pass
                else:
                    insert_list.append(i)

        if insert_list != []:
            for x in insert_list:
                notice.insert({"category" : DB_list[k] , "title": t[x], "link" : l[x], "date" : d[x]})
            ul.write(now.isoformat())
            ul.write('{0} update complate\n'.format(DB_list[k]))
        else:
            ul.write(now.isoformat())
            ul.write('{0} dose`t update\n'.format(DB_list[k]))
    ul.close()

notice_crawler()
