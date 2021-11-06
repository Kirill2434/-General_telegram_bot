
from datetime import datetime
import requests
import settings


PROXY = {
    'proxy_url': settings.proxy_url,
    'urllib3_proxy_kwargs': {
        'username': settings.PROXY_USERNAME,
        'password': settings.PROXY_PASSWORD
    }
}


class OfdClient:
    def __init__(self, login, password):
        self.login = settings.login
        self.password = settings.password

        result = requests.post(
            url='https://org.1-ofd.ru/partner-api/user/login', verify=False,
            headers=self.get_activation_headers(),
            json={'login': login, 'password': password}
        )
        self.token = result.json()['authToken']

    def get_activation_headers(self, token=None):
        headers = {'Content-Type': 'application/json'}

        if token:
            headers['X-XSRF-TOKEN'] = token
            headers['Cookie'] = f'PLAY_SESSION={token}'

        return headers

    def activate_subscription(self, reg_number, code_activate):
        result = requests.post(
            url=f'https://org.1-ofd.ru/partner-api/kkms/{reg_number}/activate-by-promo', verify=False,
            headers=self.get_activation_headers(token=self.token),
            json={'value': code_activate, 'agentCode': '7714426164'}
        )
        return result.json()


