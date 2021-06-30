#!/usr/bin/python3
import logging
import requests
import hashlib
import argparse

__author__ = "Kosterev Grigoriy <kosterev@starline.ru>"
__date__ = "13.10.2018"

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
def get_slid_user_token(app_token, user_login, user_password, output=True):
    """
     Аутентификация пользователя по логину и паролю.
     Неверные данные авторизации или слишком частое выполнение запроса авторизации с одного
     ip-адреса может привести к запросу капчи.
     Для того, чтобы сервер SLID корректно обрабатывал клиентский IP,
     необходимо проксировать его в параметре user_ip.
     В противном случае все запросы авторизации будут фиксироваться для IP-адреса сервера приложения, что приведет к частому требованию капчи.
    :param sid_url: URL StarLineID сервера
    :param app_token: Токен приложения
    :param user_login: Логин пользователя
    :param user_password: Пароль пользователя
    :return: Токен, необходимый для работы с данными пользователя. Данный токен потребуется для авторизации на StarLine API сервере.
    """
    url = 'https://id.starline.ru/apiV3/user/login/'

    payload = {
        'token': app_token
    }
    data = {}
    data["login"] = user_login
    data["pass"] = hashlib.sha1(user_password.encode('utf-8')).hexdigest()
    r = requests.post(url, params=payload, data=data)
    response = r.json()
    if output:
        logging.info('execute request: {}'.format(url))
        logging.info('payload : {}'.format(payload))
        logging.info('response info: {}'.format(r))
        logging.info('response data: {}'.format(response))
    if int(response['state']) == 1:
        slid_token = response['desc']['user_token']
        if output:
            logging.info('SLID token: {}'.format(slid_token))
        return slid_token
    raise Exception(response)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--appToken", dest="appToken", help="application identification", default="", required=True)
    parser.add_argument("-l", "--login", dest="login", help="account login", default="", required=True)
    parser.add_argument("-p", "--password", dest="password", help="account password", default="", required=True)
    parser.add_argument("-o", "--only", dest="only")
    args = parser.parse_args()
    if args.only is None:
        logging.info("appToken: {}, login: {}, password: {}".format(args.appToken, args.login, args.password))
    return args


def main():

    args = get_args()
    if args.only is None:

        get_slid_user_token(args.appToken, args.login, args.password)
    else:
        get_slid_user_token(args.appToken, args.login, args.password, output=False)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(e)