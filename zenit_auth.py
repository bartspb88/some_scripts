import re
import requests
from config import LoginData, Urls

session = requests.Session()
auth_req = session.get(Urls.ZENIT_AUTH).text
csrf = re.findall(r'content="(.{40})"', auth_req)[0]

auth_data = {
    '_token': csrf,
    'login': LoginData.EMAIL,
    'password': LoginData.PASS,
    'submit': ''
}

auth_req = session.post(Urls.ZENIT_AUTH, data=auth_data)
print(auth_req)