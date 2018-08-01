import urllib3

import json

class ElasticSearchUtil(object):
    def __init__(self):
        self.http = urllib3.PoolManager()
    
    def post(self,url,jsonData):
        encoded_data = json.dumps(jsonData).encode('utf-8')
        r = self.http.request(
            'POST',
             url,
             body = encoded_data,
             headers={'Content-Type': 'application/json'}
        )
        r.data = json.loads(r.data.decode('utf-8'))
        return r

