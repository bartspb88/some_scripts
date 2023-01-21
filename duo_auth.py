import json
import requests
from config import LoginData, Urls

data_auth = {
    'identifier': LoginData.EMAIL,
    'password': LoginData.PASS
}

session = requests.Session()
auth_req = session.post(Urls.DUO_AUTH, data=json.dumps(data_auth))
