from newsdemo.apps.crawler.esutils import ElasticSearchUtil
es = ElasticSearchUtil()

NEWSPIECE_INDEX_PATH = "http://66.42.102.161:9200/newspieces/"

class NewsPieceBase(object):
    def __init__(self,info,url):
        self.info = info
        self.url = url
    
    def save(self):
        resp = es.post(self.url,self.info)
        print('newspiece save status:',resp.status)
    
    def queryDuplicate(self,queryBody,searchUrl):
        resp = es.post(searchUrl,queryBody)
        # print(data)
        if(resp.formatted_data["hits"]["total"]>0):
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
    
    