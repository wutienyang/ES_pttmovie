# ES_pttmovie
Use Elasticsearch and Kibana to built ptt movie search service  
以此紀錄用Elasticsearch 和 Kibana建立的ptt movie的搜尋服務  
資料來源 ： ptt movie板 和 yahoo movie的電影資訊  

## auto資料夾 ( pttmovie, yahoo )
### pttmovie -   
#### auto 相關
crawler.py 爬取固定範圍的爬蟲
auto_crawler.py 自動判斷是否有新資料更新，並呼叫 crawler.py 爬取
now_index.txt 紀錄目前最新的 index ，若是有新資料 auto_crawler.py 在爬取後，會自動更新
#### 其他
pttmovie_allinsert.py 輸入 path 可以把所有資料 insert 到 Elasticsearch
test_auto_crawler.ipynb 用 jupyter notebook 來測試程式碼和指令  

### yahoomovie  

