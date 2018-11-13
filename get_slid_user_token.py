#!/usr/bin/python3
import logging
import requests
import hashlib

__author__ = "Kosterev Grigoriy <kosterev@starline.ru>"
__date__ = "13.10.2018"

def get_slid_user_token(sid_url, app_token, user_login, user_password):
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
    url = sid_url + 'user/login/'
    logging.info('execute request: {}'.format(url))
    payload = {
        'token': app_token
    }
    data = {}
    data["login"] = user_login
    data["pass"] = hashlib.sha1(user_password.encode('utf-8')).hexdigest()
    r = requests.post(url, params=payload, data=data)
    response = r.json()
    logging.info('payload : {}'.format(payload))
    logging.info('response info: {}'.format(r))
    logging.info('response data: {}'.format(response))
    if int(response['state']) == 1:
        return response['desc']['user_token']
    raise Exception(response)

if __name__ == "__main__":
    try:
        get_slid_user_token()
    except Exception as e:
        logging.error(e)