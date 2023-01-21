import requests
import json

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

auth_req = requests.post(auth_url, data=json.dumps(auth_data), headers=auth_headers)
jwt = auth_req.json()['data']['token']
grade_url = f'https://dnevnik2.petersburgedu.ru/api/journal/estimate/table?p_educations%5B%5D=424677&p_date_from=18.10.2022&p_date_to=20.10.2022&p_limit=100&p_page=1'

grade_headers = {
    'Content-Type': 'text/plain',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'cookie': f'X-JWT-Token={jwt}'
}

grade_req = requests.get(grade_url, headers=grade_headers)
grade_req_parse = grade_req.json()['data']['items']
for element in grade_req_parse:
    print(element)
    for key, value in element.items():
        print(key, value)
