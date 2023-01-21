import json
import requests
from datetime import datetime

auth_url = 'https://dnevnik2.petersburgedu.ru/api/user/auth/login'
auth_data = {
    'activation_code': None,
    'login': '',
    'password': '',
    'type': 'email',
    '_isEmpty': False
}
auth_headers = {
    'Content-Type': 'text/plain',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
auth_req = requests.post(auth_url, data=json.dumps(auth_data), headers=auth_headers)
jwt = auth_req.json()['data']['token']
homework_url = f'https://dnevnik2.petersburgedu.ru/api/journal/lesson/list-by-education?p_page=1&p_datetime_from={now}&p_datetime_to={now}&p_educations%5B%5D=424677'

homework_headers = {
    'Content-Type': 'text/plain',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'cookie': f'X-JWT-Token={jwt}'
}
homework_req = requests.get(homework_url, headers=homework_headers)
homework_req_parse = homework_req.json()['data']['items']
homework_req_parse_result = {element['subject_name']: element['tasks'] for element in homework_req_parse}

for key, value in homework_req_parse_result.items():
    if value:
        print(key, value[0]['task_name'])
