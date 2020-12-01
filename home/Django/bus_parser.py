import requests
import pymongo
from pymongo.mongo_client import MongoClient
from bs4 import BeautifulSoup
import json
client = MongoClient('222.239.90.78',30002)

db = client.chat_bot
from_school = db.from_school
from_school_sunday = db.from_school_sunday
from_station = db.from_station
from_station_sunday = db.from_station_sunday

def st():
    req = requests.get('http://sejong.korea.ac.kr/campuslife/facilities/shuttle_bus')
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    
    data1= soup.find('table',{'summary' : '고려대학교 세종캠퍼스와 조치원역 셔틀버스 안내'})
    data2= data1.findAll('td')
    NO = []
    school = []
    station = []
    
    for i in range(len(data2)):
        if i%4==0:
            NO.append(data2[i].text.strip())
        elif i%4==1:
            school.append(data2[i].text.strip())
        elif i%4==2:
            station.append(data2[i].text.strip())
        else:
            pass
        
    tsc = []
    tsc_sun = []
    tst =[]
    tst_sun =[]

    for elem in school:
        if len(elem) < 2:
            continue
        if elem[0] == '(':
            tsc_sun.append(elem[1:])
        else:
            tsc.append(elem.split("(")[0])
            if len(elem) > 5:
                tsc_sun.append(elem.split("(")[1])
                
    for idx, elem in enumerate(tsc):
        tsc[idx] = elem.strip()
        
    for idx, elem in enumerate(tsc_sun):
        tsc_sun[idx] = elem.strip()[:-1]

    for elem in station:
        if len(elem) < 2:
            continue
        if elem[0] == '(':
            tst_sun.append(elem[1:])
        else:
            tst.append(elem.split("(")[0])
            if len(elem) > 5:
                tst_sun.append(elem.split("(")[1])
                
    for idx, elem in enumerate(tst):
        tst[idx] = elem.strip()
        
    for idx, elem in enumerate(tst_sun):
        tst_sun[idx] = elem.strip()[:-1]

    return tsc, tsc_sun, tst, tst_sun


## 이 명령어는 이 파일이 import가 아닌 python에서 직접 실행할 경우에만 아래 코드가 동작하도록 합니다.
if __name__=='__main__':

    school, school_sun, station, station_sun = st()
    
    for i in range(len(school)):
        school[i]=school[i].split(':')
        
    for h, m in school:
        from_school.insert({"hour":h, "minute":m})

    for i in range(len(school_sun)):
        school_sun[i]=school_sun[i].split(':')

    for h, m in school_sun:
        from_school_sunday.insert({"hour":h, "minute":m})

    for i in range(len(station)):
        station[i]=station[i].split(':')
        
    for h, m in station:
        from_station.insert({"hour":h, "minute":m})
        
    for i in range(len(station_sun)):
        station_sun[i]=station_sun[i].split(':')
        
    for h, m in station_sun:
        from_station_sunday.insert({"hour":h, "minute":m})

#    temp = []
#
#    with open("from_shcool.json","w") as json_file:
#        for h,m in school:
#            temp.append({'hour' : h, 'minute' : m})
#        json.dump(temp, json_file)
#
#    temp = []
#    
#    with open("from_shcool_sunday.json","w") as json_file:
#        for h,m in school_sun:
#            temp.append({'hour' : h, 'minute' : m})
#        json.dump(temp, json_file)
#    
#    temp = []
#            
#    with open("from_station.json","w") as json_file:
#        for h,m in station:
#            temp.append({'hour' : h, 'minute' : m})
#        json.dump(temp, json_file)
#            
#    temp = []
#    with open("from_station_sunday.json","w") as json_file:
#        for h,m in station_sun:
#            temp.append({'hour' : h, 'minute' : m})
#        json.dump(temp, json_file)

