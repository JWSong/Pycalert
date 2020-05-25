import os
from pycalert import Alerter

if __name__ == '__main__':
    account = os.environ.get('C101_ID')
    pwd = os.environ.get('C101_PWD')

    if account is None or pwd is None:
        account = input('ID: ')
        pwd = input('password: ')

    al = Alerter(account, pwd)
    al.run()
