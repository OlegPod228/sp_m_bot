import requests
import json
import random


QIWI_TOKEN = 'be47e3330f1967598513028cadd93b14'
QIWI_ACCOUNT = '79522174779'


num = "1234567890"

def generate_random_commment():
    passw = random.sample(num,8)
    return "".join(passw)

def payments_list():
    try:
        ans = []
        s = requests.Session()
        s.headers['authorization'] = 'Bearer ' + QIWI_TOKEN
        parameters = {'rows': '50', 'operation': 'IN'}
        h = s.get('https://edge.qiwi.com/payment-history/v1/persons/' + QIWI_ACCOUNT + '/payments', params=parameters)
        req = json.loads(h.text)
        for i in range(len(req['data'])):
            ans.append(req['data'][i]['comment'])
    except Exception as e:
        print('payments_list()', e)
        return []
