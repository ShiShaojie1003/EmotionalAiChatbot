import requests
import json

class QwenService():
    def ask_stream(self,text):
        try:
            headers = {'Content-Type': 'application/json'}
            data = {"prompt": text, "history": []}
            response = requests.post(url='http://127.0.0.1:6006', headers=headers, data=json.dumps(data))
            return response.json()['response']
        except requests.exceptions.ConnectionError:
            return "好像我没有连上脑子哎，请检查一下服务器连接吧"

