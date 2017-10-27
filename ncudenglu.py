import requests,json
import re

url='https://os.ncuos.com/api/user/token'
cookies= {'_ga':'GA1.2.1236640743.1558588646','_gid':'GA1.2.1223134279.1509088595'}
headers={'content-type':'application/json'}
def denglu(id,pwd):
    postdata = {'username':id,'password':pwd}

    postdata1 = json.dumps(postdata)
    print(postdata1)
    res1 = requests.post(url,data = postdata1,headers=headers,cookies=cookies)
    res2 = res1.text
    t = re.findall('\\u83b7\\u53d6\\u6210\\u529f',res2)
    print(res2)
    if len(t) >= 1:
        return True
    else:
        return False

