#!/usr/bin/python3
import logging
import requests
import argparse


__author__ = "Kosterev Grigoriy <kosterev@starline.ru>"
__date__ = "13.10.2018"

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
def get_slnet_token(slid_token, output=True):
    """
    Авторизация пользователя по токену StarLineID. Токен авторизации предварительно необходимо получить на сервере StarLineID.
    :param slid_token: Токен StarLineID
    :return: Токен пользователя на StarLineAPI
    """
    url = 'https://developer.starline.ru/json/v2/auth.slid'

    data = {
        'slid_token': slid_token
    }
    r = requests.post(url, json=data)
    response = r.json()
    slnet_token = r.cookies["slnet"]
    if output:
        logging.info('execute request: {}'.format(url))
        logging.info('response info: {}'.format(r))
        logging.info('response data: {}'.format(response))
        logging.info('slnet token: {}'.format(slnet_token))
    return slnet_token


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--slid_token", dest="slidToken", help="StarLineID Token", default="", required=True)
    parser.add_argument("-o", "--only", dest="only")
    args = parser.parse_args()
    if args.only is None:
        logging.info("slidToken: {}".format(args.slidToken))
    return args


def main():

    args = get_args()
    if args.only is None:

        get_slnet_token(args.slidToken)
    else:
        get_slnet_token(args.slidToken, output=False)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(e)