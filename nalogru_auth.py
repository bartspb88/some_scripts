import re
import json
import requests
from bots.config import LoginData, Urls

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

first_nalog = session.head(Urls.NALOG_AUTH).headers['Location']
second_nalog = session.head(first_nalog).headers['Location']
third_nalog = session.head(second_nalog).headers['Location']
nalog_token = re.findall('token=.*(.{8}-.{4}-.{4}-.{4}-.{12}).*&has', third_nalog)
four_nalog = session.get(third_nalog)
headers = {
    'Authorization': f'Bearer {nalog_token[0]}',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
}
profile = session.get(Urls.NALOG_PROFILE, headers=headers)
