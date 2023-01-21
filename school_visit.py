import json
import time
import requests
import schedule
from config import LoginData, Urls


def telegram_bot_sendtext(token, chat_id, message):
    url = f'https://api.telegram.org/bot{token}/sendmessage?chat_id={chat_id}&parse_mode=Markdown&text={message}'
    request = requests.get(url)
    return request.text


def job():
    global key, message
    token = LoginData.TOKEN
    chat_id = LoginData.CHAT_ID

    auth_data = {
        'activation_code': None,
        'login': LoginData.DNEVNIK_LOGIN,
        'password': LoginData.DNEVNIK_PASS,
        'type': 'email',
        '_isEmpty': False
    }
    auth_headers = {
        'Content-Type': 'text/plain',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }

    auth_req = requests.post(Urls.DNEVNIK_AUTH, data=json.dumps(auth_data), headers=auth_headers)
    jwt = auth_req.json()['data']['token']

    enter_headers = {
        'Content-Type': 'text/plain',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'cookie': f'X-JWT-Token={jwt}'
    }
    enter_req = requests.get(Urls.DNEVNIK_ENTER, headers=enter_headers)
    enter_exit = enter_req.json()['data']['items']
    enter_exit_list = {element['datetime']: element['direction'] for element in enter_exit}
    for key, value in enter_exit_list.items():
        if value == 'output':
            message = f'Вышел из школы: {key}'
        else:
            message = f'Вошел в школу: {key}'

    key_file = open('key_file.txt', 'r')
    if key != key_file.read():
        telegram_bot_sendtext(token, chat_id, f'{message}')
    key_file.close()
    key_file = open('key_file.txt', 'w+')
    key_file.write(key)
    key_file.close()


schedule.every(1).hour.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
