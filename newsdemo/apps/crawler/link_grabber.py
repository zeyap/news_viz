import pprint
import urllib3
http = urllib3.PoolManager()
import json
from urllib.parse import urlencode
from newsdemo.settings.local import API_KEY, CX_CODE

def getlink(headline):

    params = {
            'key':API_KEY,
            'q': headline,
            'cx':CX_CODE,
            'num':'3',
            'fields':'items(title, link)'
        }
    
    url = 'https://www.googleapis.com/customsearch/v1'

    r = http.request(
        'GET',
        url,
        fields = params
        # body = json.dumps(body).encode('utf-8'),
        # headers={'Content-Type': 'application/json'}
    )

    decoded = json.loads(r.data.decode('utf-8'))
    # print(decoded)
    return decoded['items']