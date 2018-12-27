#!/usr/bin/python3
import logging
import argparse

from get_app_code import get_app_code
from get_app_token import  get_app_token
from get_slid_user_token import get_slid_user_token
from get_slnet_token import get_slnet_token

__author__ = "Kosterev Grigoriy <kosterev@starline.ru>"
__date__ = "13.10.2018"


def auth(app_id, app_secret, login, password):
    # Получим код приложения
    app_code = get_app_code(app_id, app_secret)

    # Получим токен приложения. Действителен 4 часа
    app_token = get_app_token(app_id, app_secret, app_code)

    # Получим slid-токен юзера. Действителен 1 год
    slid_token = get_slid_user_token(app_token, login, password)

    # Пройдем авторизацию на StarLineAPI сервере
    # С полученным токеном можно обращаться к API-метода сервера StarLineAPI
    # Токен действителен 24 часа
    slnet_token = get_slnet_token(slid_token)
    return slnet_token


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--appId", dest="appId", help="application identifier", default="", required=True)
    parser.add_argument("-s", "--appSecret", dest="appSecret", help="application secret", default="", required=True)
    parser.add_argument("-l", "--login", dest="login", help="account login", default="", required=True)
    parser.add_argument("-p", "--password", dest="password", help="account password", default="", required=True)
    args = parser.parse_args()
    logging.info('appId: {}, appSecret: {}, login: {}, password: {}'.format(args.appId, args.appSecret, args.login, args.password))
    return args


def main():
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    args = get_args()
    auth(args.appId, args.appSecret, args.login, args.password)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(e)
