# ES_pttmovie
Use Elasticsearch and Kibana to built ptt movie search service  
以此紀錄用Elasticsearch 和 Kibana建立的ptt movie的搜尋服務  
資料來源 ： ptt movie板 和 yahoo movie的電影資訊  
## 開啟 elasticsearch & kibana
更改 elasticsearch ip  
`vim config/elasticsearch.yml`  
network.host : your ip  
更改 kibana ip  
`vim config/kibana.yml`  
server.host : your ip  
elasticsearch.url: "http://yourip:9200/"  
1. bin/elasticsearch
2. bin/kibana  

p.s kibana 是透過 elasticsearch.url 去讀 elasticsearch 的資料  

## pttscore folder
### module
#### 把 pttscore 包裝成 module (可以 import 使用)
word_dic 好雷，壞雷字典，記載屬於好雷或是壞雷的詞彙，算 pttscore 會使用到  
__init__.py  讓 pttscore.py 可以成為 module  
pttscore.py ptt movie 分數的算法  
test_pttscore.ipynb 測試 pttscore.py 的使用情形  

### analysis
score.ipynb 用 jupyter notebook 來探索各個指標和更新演算法

## auto folder ( pttmovie, yahoo )
### pttmovie -   
#### auto
crawler.py 爬取固定範圍的爬蟲  
auto_crawler.py 自動判斷是否有新資料更新，並呼叫 crawler.py 爬取  
now_index.txt 紀錄目前最新的 index ，若是有新資料 auto_crawler.py 在爬取後，會自動更新  
json folder 存放爬蟲爬到的資料  

#### log
script_log.txt 由 auto_crawler.py 判斷是否該寫入 (e.g. 有更新或是沒更新都把紀錄寫進去)  
crontab.log 由 corntab -e 執行排程所寫入，判斷定時排程是否正確  

#### 其他
pttmovie_allinsert.py 輸入 path 可以把所有資料 insert 到 Elasticsearch  
test_auto_crawler.ipynb 用 jupyter notebook 來測試程式碼和指令  


### yahoomovie -  
#### auto
crawler.py 爬取固定範圍的爬蟲  
auto_crawler.py 自動判斷是否有新資料更新，並呼叫 crawler.py 爬取  
now_index.txt 紀錄目前最新的 index ，若是有新資料 auto_crawler.py 在爬取後，會自動更新  

#### log
script_log.txt 由 auto_crawler.py 判斷是否該寫入 (e.g. 有更新或是沒更新都把紀錄寫進去)  
crontab.log 由 corntab -e 執行排程所寫入，判斷定時排程是否正確  

#### 其他
test_auto_crawler.ipynb 用 jupyter notebook 來測試程式碼和指令  
pickle & images folder 存放爬蟲爬到的資料  
 
## search_example.ipynb
用 Elasticsearch 搜尋的語法和結果  

## crontab_job.txt
執行 auto_crawler 的語法  

## cmd_curl.txt
用 bash 去對 Elasticsearch 進行操作(e.g. put mapping, delete, count query...)  
