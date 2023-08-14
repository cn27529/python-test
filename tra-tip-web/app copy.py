#elements startStation endStation rideDate startTime endTime

import requests
from bs4 import BeautifulSoup
import json
import argparse
import sys
import time
from pathlib import Path
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

#print("參數範例：3160-苗栗 4080-嘉義 2023/08/12")
#input_startStation = str(input('輸入起站：'))
#input_endStation = str(input('輸入迄站：'))
#input_rideDate = str(input('輸入日期yyyy/mm/dd：'))

print (sys.argv)
argv_len = len(sys.argv)

print("請稍候...")
time.sleep(3)

is_run = False

input_s1 = ''
input_s2 = ''
input_ymd = ''
path = Path('.')

if argv_len == 4:
    input_s1 = sys.argv[1]
    input_s2 = sys.argv[2]
    input_ymd = sys.argv[3]
    is_run = True
else :
    #print("確認參數如：3300-臺中 3160-苗栗 2023/09/09")
    input_s1 = "4080-嘉義"
    input_s2 = "3160-苗栗"
    input_ymd = "2023/09/09"
    is_run = True

#print(is_run)
class TrainProps:
  def __init__(self, s1, s2, ymd):
    self.input_s1 = s1
    self.input_s2 = s2
    self.input_ymd = ymd

props = TrainProps(input_s1, input_s2, input_ymd)

def go_search(props):
    url = "https://tip.railway.gov.tw/tra-tip-web/tip/tip001/tip112/querybytime?transfer=ONE&trainTypeList=ALL&startOrEndTime=true&queryClassification=NORMAL&startStation={0}&endStation={1}&rideDate={2}&startTime=00:00&endTime=23:59&sort=departureTime,asc".format(props.input_s1, props.input_s2, props.input_ymd)
    res = requests.get(url)
    res.encoding = "utf-8"

    soup = BeautifulSoup(res.text, "html.parser")

    train_item = soup.select(".trip-column")
    train_item_len = len(train_item)
    jsonString = '[';
    for index in range(len(train_item)):
        values = train_item[index].text.split('\n')
        values_len = len(values)
        uid = '{ "uid": %s, ' % str(index)
        trainNumber = '"trainNumber": "%s", ' % values[5]
        startStation = '"startStation": "%s", ' % values[7]
        endStation = '"endStation": "%s", ' % values[9]
        startTime = '"startTime": "%s", ' % values[15]
        endTime = '"endTime": "%s", ' % values[16]
        trainTime = '"trainTime": "%s", ' % values[17]
        trainLine = '"trainLine": "%s", ' % values[18]
        allPrice = '"allPrice": "%s", ' % values[25]
        childPrice = '"childPrice": "%s", ' % values[29]
        oldPrice = '"oldPrice": "%s" }' % values[33]
        
        string_format = uid + trainNumber+ startStation+ endStation + startTime + endTime + trainTime + trainLine + allPrice + childPrice + oldPrice

        jsonString += string_format

        if index < train_item_len-1:
            jsonString+=','

    jsonString+=']' #end jsonString
    jsonData = json.loads(jsonString)

    write_firebase_firestore(jsonData)

    print(jsonData)
    print("共%s筆，查詢結束。" % len(jsonData))
    

def write_firebase_firestore(data):
    
    # Use a service account.
    path = Path('')
    isfile = path.is_file()
    firebase_json = ''
    cred = credentials.Certificate(firebase_json)
    app = firebase_admin.initialize_app(cred)
    db = firestore.client()
    #doc = db.collection("train_collection").document("tra_tip_data")
    
    for index in range(len(data)):
        item_data = data[index]
        #doc = db.collection("train_collection").document("tra_tip_data")
        doc_name = ''
        if index <= 9:
            doc_name = '0%s' % str(index)
        else:
            doc_name = str(index)
        #doc = db.collection("train_collection").document("tra_tip_data"+doc_name)
        doc = db.collection("train_collection").document()
        doc.set(item_data, merge=True)
    

if is_run :
    go_search(props)

