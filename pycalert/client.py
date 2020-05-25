import requests
import json


class Class101Client:
    def __init__(self, id, password):
        self.id = id
        self.password = password
        self.req_url = 'https://www.googleapis.com/identitytoolkit/v3/relyingparty/' \
                       'verifyPassword?key=AIzaSyBOybGuB69OpLttriljMZUvEpdFXTqahFY'
        self.headers = {
            'authority': 'www.googleapis.com',
            'x-client-version': 'Chrome/JsCore/4.13.0/FirebaseCore-web',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
            'content-type': 'application/json',
            'accept': '*/*',
            'origin': 'https://creator.class101.net',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'accept-language': 'ko,en-US;q=0.9,en;q=0.8'
        }
        self.token = ''
        self.login()

    def login(self):
        data = {
            "email": self.id,
            "password": self.password,
            "returnSecureToken": True
        }
        res = requests.post(self.req_url, headers=self.headers, data=json.dumps(data).encode()).json()

        self.token = res['idToken']

    def data_query(self, data):
        url = 'https://gql-prod.class101.net/graphql'
        data = json.dumps(data).encode()
        headers = {
            'authorization': f'Bearer {self.token}',
            'authority': 'gql-prod.class101.net',
            'accept': '*/*',
            'environment': 'ADMIN',
            'x-transaction-id': '20f3114a-128a-4e4b-9405-38b5d7932d43',
            'apollographql-operation-type': 'query',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/81.0.4044.138 Safari/537.36',
            'content-type': 'application/json',
            'origin': 'https://creator.class101.net',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://creator.class101.net/creator/posts/klass?productId=5e2556a44ba7b950bbd46bb5',
            'accept-language': 'ko,en-US;q=0.9,en;q=0.8'
        }

        res = requests.post(url, headers=headers, data=data)

        return res
