import json
import time
from elasticsearch import Elasticsearch

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
        
    es = Elasticsearch([{'host': 'teadaiegpu1.hopto.org', 'port': 9200}])
    for t in tmp:
        print t['url']
        es.index(index='pttmovie', doc_type='content', body=t)

def insert_main(paths):
    for path in paths:
        print (path)
        with open(path) as data_file:    
            data = json.load(data_file)
            insert(data)

path_part1 = ['movie-5001-5851.json','movie-4001-5000.json', 'movie-3001-4000.json', 'movie-2001-3000.json', 'movie-1001-2000.json', 'movie-1-1000.json']
path_part2 = 'movie_1-5851/'
paths = [path_part2+p for p in path_part1]
insert_main(paths)