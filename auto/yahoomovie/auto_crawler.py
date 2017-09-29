import os
import requests
from bs4 import BeautifulSoup
from subprocess import Popen
from datetime import datetime

es = Elasticsearch([{'host': 'teadaiegpu1.hopto.org', 'port': 9200}])

def insert_main(paths):
    for path in paths:
        with open(path, 'rb') as handle:
            contents = pickle.load(handle)
            noerror = []
            for c in contents:
                if 'error' not in c.keys():
                    if c['IMDb'] != None:
                        c['IMDb'] = float(c['IMDb'])
                    noerror.append(c)
            for t in noerror:
                es.index(index='yahoomovie', doc_type='content', body=t)
                
# load now index
with open('now_index.txt', 'r') as f:
    now_index = f.readlines()
now_index = int(now_index[0].strip())
            
# chech if new index have
def check_is(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    div = soup.find("div", "movie_intro_info_r")
    if div != None:
        return True
    else:
        return False

# first
triggle = check_is('https://tw.movies.yahoo.com/movieinfo_main.html/id='+str(now_index+1)+'.html')
datetimestr =  datetime.now().strftime("%Y-%m-%d %H:%M:%S")

if triggle:
    now_index_list = []
    while triggle:
        url = 'https://www.ptt.cc/bbs/movie/index'+str(now_index)+'.html'
        triggle = check_is(url)
        if triggle:
            now_index_list.append(now_index)
            now_index+=1
    icmd = str(now_index_list[0]+1)+' '+str(now_index_list[-1])
    cmd = '/home/yang/anaconda2/envs/python2/bin/python crawler.py '+icmd
    os.system( cmd )
    # run script log in script_log
    with open('./log/script_log.txt', 'a') as f:
        f.write(datetimestr+'   '+cmd+'\n')
    # update now index
    with open('now_index.txt', 'w') as f:
        f.write(str(now_index_list[-1]))
    # insert elasticsearch
    path_to_pickle = os.getcwd()
    paths = [pos_pickle for pos_pickle in os.listdir(path_to_pickle) if pos_pickle.endswith('.pickle')]
    insert_main(paths)
    # move 
    os.system( 'mv *.pickle ./pickle/' )
    
else:
    # no run script log in script_log
    with open('./log/script_log.txt', 'a') as f:
        f.write(datetimestr+'   '+'no run script'+'\n')    