import urllib3
http = urllib3.PoolManager()

import json

NEWSPIECE_INDEX_PATH = "http://66.42.102.161:9200/newspieces/"

class NewsPieceBase(object):
    def __init__(self,info,url):
        self.info = info
        self.url = url
    
    def save(self):
        encoded_data = json.dumps(self.info).encode('utf-8')
        r = http.request(
            'POST',
             self.url,
             body = encoded_data,
             headers={'Content-Type': 'application/json'})
        print('newspiece save status:',r.status)
    
    def queryDuplicate(self,queryBody,searchUrl):
        encoded_data = json.dumps(queryBody)
        r = http.request(
            'POST',
            searchUrl,
            body = encoded_data,
            headers={'Content-Type': 'application/json'})
        data = json.loads(r.data.decode('utf-8'))
        # print(data)
        if(data["hits"]["total"]>0):
            return False
        else:
            return True
            

class StandardNewsPiece(NewsPieceBase):
    def __init__(self,info):
        self.searchUrl = NEWSPIECE_INDEX_PATH+"_search"
        self.indexingUrl = NEWSPIECE_INDEX_PATH+'doc?pretty'
        super(StandardNewsPiece,self).__init__(info,self.indexingUrl)
        # print('newspiece init')

    def queryDuplicate(self):
        queryBody={
            "query":{"match":{"author":self.info["author"]}}
        }
        return super(StandardNewsPiece,self).queryDuplicate(queryBody,self.searchUrl)
    
    def save(self):
        if True == self.queryDuplicate():
            super(StandardNewsPiece,self).save()
        else:
            print("a duplicate record already exist")
    
    