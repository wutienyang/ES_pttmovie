
# coding: utf-8

# In[8]:

import requests
from bs4 import BeautifulSoup
import pickle
from multiprocessing import Pool
import time
from time import sleep
import sys
# In[2]:

class YahooMovieCrawler(object):
    def __init__(self):
        self.start = int(sys.argv[1])
        self.end = int(sys.argv[2])+1
        urls = ['https://tw.movies.yahoo.com/movieinfo_main.html/id='+str(a) for a in range(self.start,self.end)]
        
        start_time = time.time()
        contents = []
        for u in urls:
            contents.append(self.crawler(u))
        end_time = time.time()

        print ("run time : {}").format(end_time - start_time)

        error = 0
        for a in contents:
            if 'error' in a.keys():
                error+=1
        path = 'contents_'+str(self.start)+'_'+str(self.end-1)+'.pickle'
        with open(path, 'wb') as handle:
            pickle.dump(contents, handle, protocol=pickle.HIGHEST_PROTOCOL)

        print ("all count : {}").format(len(contents))
        print ("error count : {}").format(error)


    
    def crawler(self, url):
        print url
        sleep(0.1)
        content = {}
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        div = soup.find("div", "movie_intro_info_r")
        div_l = soup.find("div", "movie_intro_info_l")
        if div != None:
            content['url'] = url
            try:
                content['name_zh'] = div.h1.string.encode('utf8')
            except:
                content['name_zh'] = None
            try:
                content['name_en'] = div.h3.string.encode('utf8')
            except:
                content['name_en'] = None
            try:
                content['tags'] = [ a.a.string.strip().encode('utf8') for a in div.find("div", "level_name_box").find_all("div", "level_name") ]
            except:
                content['tags'] = None
            try:
                content['director'] = div.find_all("div", "movie_intro_list")[0].string.strip().encode('utf8')
            except:
                content['director'] = None
            try:
                content['actor'] = [ a.string.encode('utf8') for a in div.find_all("div", "movie_intro_list")[1].find_all("a") ]
            except:
                content['actor'] = None


            span_list = [ a.string.encode('utf8') for a in div.find_all("span") ]
            info = {}
            for a in span_list:
                tmp = a.split('：')
                if tmp[0] == '上映日期':
                    info['create date'] = tmp[1]
                elif tmp[0] == '片　　長':
                    info['movie time'] = tmp[1]
                elif tmp[0] == '發行公司':
                    info['company'] = tmp[1]
                elif tmp[0] == 'IMDb分數':
                        info['IMDb'] = tmp[1]
            try:
                content['create date'] = info['create date'].encode('utf8')
            except:
                content['create date'] = None
            try:
                content['movie time'] = info['movie time'].encode('utf8')
            except:
                content['movie time'] = None
            try:
                content['company'] = info['company'].encode('utf8')
            except:
                content['company'] = None

            try:
                content['IMDb'] = info['IMDb'].encode('utf8')
            except:
                content['IMDb'] = None

            image_url = div_l.find('img')['src']
            img_data = requests.get(image_url).content
            try:
                with open('pickle/images/'+content['name_zh']+'.jpg', 'wb') as handler:
                    handler.write(img_data)
            except:
                pass
            return content
        else:
            return {'error' : url}
        
if __name__ == '__main__':
    c = YahooMovieCrawler()




