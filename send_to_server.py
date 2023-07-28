import urllib
from urllib.parse import urlencode
from urllib.request import urlopen
from urllib.request import Request

import requests
import json

def send_to_server(data):
    data=urlencode(data).encode("utf-8")
    path='https://messenger.atu.kz/controllers/index.php'
    # print(data)
    req=Request(path, data)
    req.add_header("Content-type", "application/x-www-form-urlencoded; charset=utf-8")
    response=urlopen(req).read().decode('utf-8')
    print(response)
    try:
        return json.loads(response)
    except:
        pass
    # if response['name'] == 'link':
    #     send
    
if __name__ == "__main__":
    # data = {
    #         'id' : 1,
    #         'func' : 'contacts_json',
    #         'messenger' : 'telegram',
    #         'data': [
    #             {
    #                 '1id' : 1,
    #                 '1func' : 'contacts_json',
    #                 '1messenger' : 'telegram',
    #                 '1data': 1,
    #             },
    #             {
    #                 '1id' : 1,
    #                 '1func' : 'contacts_json',
    #                 '1messenger' : 'telegram',
    #                 '1data': 1,
    #             },
    #             {
    #                 '1id' : 1,
    #                 '1func' : 'contacts_json',
    #                 '1messenger' : 'telegram',
    #                 '1data': 1,
    #             }
    #         ],
    #     }
    # send_to_server(data)
    print("Hello, World!")