#!/usr/bin/python3
import logging
import argparse

from get_app_code import get_app_code
from get_app_token import  get_app_token
from get_slid_user_token import get_slid_user_token
from slapi_auth import slapi_auth

__author__ = "Kosterev Grigoriy <kosterev@starline.ru>"
__date__ = "13.10.2018"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--appId", dest="appId", help="application identifier", default="", required=True)
    parser.add_argument("-c", "--appCode", dest="appCode", help="application code", default="", required=True)
    parser.add_argument("-l", "--login", dest="login", help="account login", default="", required=True)
    parser.add_argument("-p", "--password", dest="password", help="account password", default="", required=True)
    args = parser.parse_args()
    print(args.appId)
    print(args.appCode)
    print(args.login)
    print(args.password)


"""
    ### Входные данные ###
    app_secret = "sc9TbCGTyN6NqG5s0FQG7fHCklNuiPkU"       # Пароль приложения
    app_id = 2                                           # ID приложения
    login = "varakin.1@mail.ru"                         # Логин аккаунта
    password = "1234Qwer"                               # Пароль от аккаунта
    sid_url = 'https://id.starline.ru/apiV3/'  # URL StarLineID сервера
    slapi_url = 'https://dev.starline.ru/'   # URL StarLineAPI сервера


    ### Прохождение аутентификации в системе StarLine ####
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

    # Получим код приложения
    app_code = get_app_code(sid_url, app_id, app_secret)
    # Получим токен приложения. Действителен 4 часа
    app_token = get_app_token(sid_url, app_id, app_secret, app_code)
    # Получим slid-токен юзера. Действителен 1 год
    slid_token = get_slid_user_token(sid_url, app_token, login, password)

    logging.info('SLID token: {}'.format(slid_token))

    # Пройдем авторизацию на StarLineAPI сервере
    # С полученным токеном можно обращаться к API-метода сервера StarLineAPI
    # Токен действителен 24 часа
    slnet_token = slapi_auth(slapi_url, slid_token)
    logging.info('slnet token: {}'.format(slnet_token))
    logging.info('ok.')
    
"""

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(e)
