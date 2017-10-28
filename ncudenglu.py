import requests,json
import re

url='https://os.ncuos.com/api/user/token'
cookies= {'_ga':'GA1.2.1236640743.1558588646','_gid':'GA1.2.1223134279.1509088595'}
headers={'content-type':'application/json'}
def login(id,pwd):
    print('pwd============',pwd)
    postdata = {'username':id,'password':pwd}

    postdata1 = json.dumps(postdata)
    res = requests.post(url,data = postdata1,headers=headers,cookies=cookies).text
    res = json.loads(res)
    if res['message'] == '获取成功':
        return res
    else:
        return 'unknownerror'

def get_info(token):

    url_index = 'https://os.ncuos.com/api/user/profile/index'
    headers_index = {'Authorization':'passport '+ token}

    res_index = requests.get(url_index,cookies=cookies,headers=headers_index).text
    print(res_index)
    res_index = json.loads(res_index)
    return res_index

