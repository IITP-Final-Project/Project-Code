import requests
import os
import django
import datetime
from bs4 import BeautifulSoup

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bot.settings")
django.setup()

from parsed_data.models import corona_prevent_notice, corona_action_notice, common_notice, event_notice, career_notice, scholarship_notice, weekly_menu

def notice_crawler():
    notice_list=['http://sejong.korea.ac.kr/user/boardList.do?handle=102914&siteId=kr&id=kr_050108010000','http://sejong.korea.ac.kr/user/boardList.do?handle=101685&siteId=kr&id=kr_050108020000','http://sejong.korea.ac.kr/campuslife/notice/college','http://sejong.korea.ac.kr/user/boardList.do?handle=61751&siteId=kr&id=kr_050107000000','http://sejong.korea.ac.kr/campuslife/notice/scholarship','http://sejong.korea.ac.kr/campuslife/notice/career']
    DB_list =[corona_prevent_notice, corona_action_notice, common_notice, event_notice, scholarship_notice, career_notice]
    ul = open('/home/Django/update_log.txt', 'a')
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
            d.append(datetime.datetime.strptime(data3[j], "%Y-%m-%d").date())
            l.append("http://sejong.korea.ac.kr" + str(data4[i]).split('"')[1])  
        t.reverse()
        l.reverse()
        d.reverse()
        
        temp = DB_list[k].objects.all()
        last_notice = DB_list[k].objects.filter(date=temp[len(temp)-1].date)
        last_notice_title = []

        for i in last_notice:
            last_notice_title.append(i.title)
        
        insert_list =[]
        
        if __name__ == '__main__':
            for h in range(len(d)):
                if d[h] > temp[len(temp)-1].date:
                    insert_list.append(h)
                elif d[h] < temp[len(temp)-1].date:
                    pass
                else:
                    if t[h] in last_notice_title:
                        pass
                    else:
                        insert_list.append(h)
        if insert_list != []:
            for x in range(len(t)):
                DB_list[k].objects.create(title=t[x], link=l[x], date=d[x])
            ul.write(now.isoformat())
            u;wirte('{0} update complate\n'.format(DB_list[k]))
        else:
            ul.write(now.isoformat())
            ul.write('{0} nothing update\n'.format(DB_list[k]))
    ul.close()

def weeklymenu():
    ul = open('/home/Django/update_log.txt', 'a')
    now = datetime.datetime.now()
    
    req = requests.get('http://sejong.korea.ac.kr/campuslife/facilities/dining/weeklymenu')
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    
    data1= soup.find('span',{'class' : 'buttonGo floatR'})
    data2 = data1.find('a')
    l=str(data2).split('"')[1]
    
    temp = weekly_menu.objects.last()
    if l == temp.link:
        pass
        
    else:
        weekly_menu.objects.create(link = l)
    ul.close()

#notice_crawler()
weeklymenu()
