import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import time
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'teadaiegpu1.hopto.org', 'port': 9200}])

def month(m):
    if m == 'Jan':
        return '01'
    elif m == 'Feb':
        return '02'
    elif m == 'Mar':
        return '03'
    elif m == 'Apr':
        return '04'
    elif m == 'May':
        return '05'
    elif m == 'Jun':
        return '06'
    elif m == 'Jul':
        return '07'
    elif m == 'Aug':
        return '08'
    elif m == 'Sep':
        return '09'
    elif m == 'Oct':
        return '10'
    elif m == 'Nov':
        return '11'
    elif m == 'Dec':
        return '12'

def daily(d):
    d = d.strip()
    if 1 <= int(d) <=9:
        return '0'+d
    else:
        return d
def map_month(m):
    m = m.split(' ')
    if len(m) == 5:
        return m[-1]+'-'+month(m[1])+'-'+m[2]+' '+m[3]
    elif len(m) == 6:
        return m[-1]+'-'+month(m[1])+'-0'+m[3]+' '+m[4]

def insert(data):
    # delete error
    tmp = [ d for d in data['articles'] if d != {u'error': u'invalid url'}]

    for i, v in enumerate(tmp):
        tmp_date = v['date']
        # week
        try:
            tmp[i]['week'] = tmp_date.split(' ')[0]
        except:
            tmp[i]['week'] = None

        # date
        try:
            tmp[i]['date'] = map_month(tmp_date)
        except:
            tmp[i]['date'] = None

        # ip
        if v['ip'] == 'None':
            tmp[i]['ip'] = None
        
    for t in tmp:
        print t['url']
        es.index(index='pttmovie', doc_type='content', body=t)

def insert_main(paths):
    for path in paths:
        print (path)
        with open(path) as data_file:    
            data = json.load(data_file)
            insert(data)

# load now index
with open('now_index.txt', 'r') as f:
    now_index = f.readlines()
now_index = int(now_index[0].strip())

# chech if new index have
def check_is(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    divs = soup.find("div", "btn-group-paging")
    live = divs.find_all("a", "disabled")
    if live == []:
        return True
    else:
        return False


# first
triggle = check_is('https://www.ptt.cc/bbs/movie/index'+str(now_index+1)+'.html')
datetimestr =  datetime.now().strftime("%Y-%m-%d %H:%M:%S")

if triggle:
    now_index_list = []
    while triggle:
        url = 'https://www.ptt.cc/bbs/movie/index'+str(now_index)+'.html'
        triggle = check_is(url)
        if triggle:
            now_index_list.append(now_index)
            now_index+=1
    icmd = ' -i '+str(now_index_list[0]+1)+' '+str(now_index_list[-1])
    cmd = '/home/yang/anaconda2/envs/python2/bin/python crawler.py -b movie'+icmd
    os.system( cmd )
    # run script log in script_log
    with open('./log/script_log.txt', 'a') as f:
        f.write(datetimestr+'   '+cmd+'\n')
    # update now index
    with open('now_index.txt', 'w') as f:
        f.write(str(now_index_list[-1]))
    # insert elasticsearch
    path_to_json = os.getcwd()
    paths = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    insert_main(paths)
    os.system( 'mv *.json ./json/' )        
else:
    # no run script log in script_log
    with open('./log/script_log.txt', 'a') as f:
        f.write(datetimestr+'   '+'no run script'+'\n')  

