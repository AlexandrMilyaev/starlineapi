#!/usr/bin/python3
import logging
import requests
import hashlib
import argparse

__author__ = "Kosterev Grigoriy <kosterev@starline.ru>"
__date__ = "13.10.2018"

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
def get_app_code(app_id, app_secret, output=True):
    """
    Получение кода приложения для дальнейшего получения токена.
    Идентификатор приложения и пароль выдаются контактным лицом СтарЛайн.
    Срок годности кода приложения 1 час.
    :param app_id: Идентификатор приложения
    :param app_secret: Пароль приложения
    :return: Код, необходимый для получения токена приложения
    """
    url = 'https://id.starline.ru/apiV3/application/getCode/'

    payload = {
        'appId': app_id,
        'secret': hashlib.md5(app_secret.encode('utf-8')).hexdigest()
    }
    r = requests.get(url, params=payload)
    response = r.json()
    if output:
        logging.info('execute request: {}'.format(url))
        logging.info('payload : {}'.format(payload))
        logging.info('response info: {}'.format(r))
        logging.info('response data: {}'.format(response))
    if int(response['state']) == 1:

        app_code = response['desc']['code']
        if output:
            logging.info('Application code: {}'.format(app_code))
        return app_code
    raise Exception(response)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--appId", dest="appId", help="application identifier", default="", required=True)

    parser.add_argument("-s", "--appSecret", dest="appSecret", help="account secret", default="", required=True)
    parser.add_argument("-o", "--only", dest="only")

    args = parser.parse_args()
    if args.only is None:
        logging.info('appId: {}, appSecret: {}'.format(args.appId, args.appSecret))
    return args


def main():

    args = get_args()
    if args.only is None:

        get_app_code(args.appId, args.appSecret)
    else:
        get_app_code(args.appId, args.appSecret, output=False)



if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(e)