#!/usr/bin/python3
import logging
import requests

__author__ = "Kosterev Grigoriy <kosterev@starline.ru>"
__date__ = "13.10.2018"

def slapi_auth(slapi_url, slid_token):
    """
    Авторизация пользователя по токену StarLineID. Токен авторизации предварительно необходимо получить на сервере StarLineID.
    :param slapi_url:   URL StarLineAPI сервера
    :param slid_token: Токен StarLineID
    :return: Токен пользователя на StarLineAPI
    """
    url = slapi_url + 'json/v2/auth.slid'
    logging.info('execute request: {}'.format(url))
    data = {
        'slid_token': slid_token
    }
    r = requests.post(url, json=data)
    response = r.json()
    logging.info('response info: {}'.format(r))
    logging.info('response data: {}'.format(response))
    return r.cookies["slnet"]

if __name__ == "__main__":
    try:
        slapi_auth()
    except Exception as e:
        logging.error(e)