import requests
import datetime
from pymongo.mongo_client import MongoClient
import json
from bs4 import BeautifulSoup

client = MongoClient('222.239.90.78',30002)

db=client.chat_bot
wm = db.weekly_menu

def weeklymenu():
    now = datetime.datetime.now()
    
    req = requests.get('http://sejong.korea.ac.kr/campuslife/facilities/dining/weeklymenu')
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    data1= soup.find('span',{'class' : 'buttonGo floatR'})
    data2 = data1.find('a')
    l='http://sejong.korea.ac.kr'+str(data2).split('"')[1]
    
    wm.insert({"link" : l})
    
#    with open("weeklymenu.json" , "a") as json_file:
#        json.dump({"link" :l}, json_file)
weeklymenu()
