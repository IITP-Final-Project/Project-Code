import requests
import datetime
import json
from pymongo.mongo_client import MongoClient
from bs4 import BeautifulSoup

client = client = MongoClient('222.239.90.78',30002)

db = client.chat_bot
club_intro = db.club_intro

def club_crawler():
    category = ['science_technology','volunteer_activities','stage_arts','exhibition_creation','religion','physical','acadmic']
    temp = []
    for i in range(len(category)):
        now = datetime.datetime.now()
        req = requests.get('https://sejong.korea.ac.kr/campuslife/student/clubs/'+category[i])
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')

        data1 = soup.findAll('div', {'class' : 'text'})
        for j in data1:
            data2= j.findAll('p',{'class' : 'marB20'})
            l=''
            for k in data2:
                k = k.text.strip()
                k = k.replace('\n','')
                k = k.replace('\t','')
                l = l + k +'\n\n'
            temp.append({"category" : category[i], "name":j.h4.text, "explanation":l})
    with open("club_intro.json","a") as json_file:
        json.dump(temp, json_file)
            
#            club_intro.insert({"category":category[i], "name":j.h4.text, "explanation":l})
club_crawler()
