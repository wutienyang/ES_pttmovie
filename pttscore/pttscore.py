# -*- encoding: utf-8 -*-
import requests  
import json
import re

class Pttscore(object):
    def __init__(self):
        with open('word_dic/bad_words.txt', 'r') as f:
            self.bad_words = f.readlines()
            self.bad_words = [w.strip() for w in self.bad_words]

        with open('word_dic/good_words.txt', 'r') as f:
            self.good_words = f.readlines()
            self.good_words = [w.strip() for w in self.good_words]
        
    def search(self, url, term):
        """Simple Elasticsearch Query"""
        query = json.dumps({
            "query": {
                "match_phrase": {
                    "article_title": term
                }
            },
            "size":1500
        })
        response = requests.get(url, data=query)
        results = json.loads(response.text)
        return results

    def parse_title(self, title):
        try:
            tmp_title = re.search(r"\[(.*?)\]", title).group().encode('utf8')
            if '雷' in tmp_title:
                if tmp_title in self.good_words:
                    return 'g'
                if tmp_title in self.bad_words:
                    return 'b'
                else:
                    return 'n'
        except:
            return None

    def score(self, search_text):
        uri_search = 'http://teadaiegpu1.hopto.org:9200/pttmovie/_search'
        results = self.search(uri_search, search_text)

        results = results['hits']['hits']
        titles = [v['_source']['article_title'] for v in results]
        message_conut = [v['_source']['message_conut'] for v in results]

        # {u'all': 12, u'boo': 1, u'count': 8, u'neutral': 2, u'push': 9}
        g_content = []
        b_content = []
        n_content = []
        for t, message in zip(titles, message_conut):
            sign = self.parse_title(t)
            if sign == 'g':
                g_content.append(message)
            elif sign == 'b':
                b_content.append(message)
            elif sign == 'n':
                n_content.append(message)
        n = len(g_content) + len(b_content) + len(n_content)
    #     print 'g: {}, b: {}, n: {} '.format(len(g_content),len(b_content),len(n_content))
        verfify_g_content = []
        verfify_b_content = []
        for a in  g_content:
            if a['boo'] > a['push']:
                verfify_b_content.append(a)
            elif a['boo'] == a['push']:
                n_content.append(a)
            else:
                verfify_g_content.append(a)
        for a in b_content:
            if a['boo'] > a['push']:
                verfify_g_content.append(a)
            elif a['boo'] == a['push']:
                n_content.append(a)
            else:
                verfify_b_content.append(a)
        verfify_n = len(verfify_g_content) + len(verfify_b_content) + len(n_content)
    #     print 'g: {}, b: {}, n: {} '.format(len(verfify_g_content),len(verfify_b_content),len(n_content))
    #     for t in titles:
    #         print t
        return round(len(verfify_g_content)/float(verfify_n+1)*10, 1)