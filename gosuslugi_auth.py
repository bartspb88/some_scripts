import json
import requests
from config import LoginData, Urls

session = requests.Session()

first_redir = session.head(Urls.GOSUSLUGI_START).headers['Location']
second_redir = session.head(f'https:{first_redir}').headers['Location']
third_redir = session.head(second_redir)

data = {
    'idType': 'email',
    'login': LoginData.EMAIL,
    'password': LoginData.GOSUSLUGI_PASS
}
headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
}
auth_req = session.post(Urls.GOSUSLUGI_AUTH, data=json.dumps(data), headers=headers)
gosuslugi_token = auth_req.json()['redirect_url']

auth_redir = session.head(gosuslugi_token).headers['Location']
final_auth = session.get(auth_redir)
