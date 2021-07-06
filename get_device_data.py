#!/usr/bin/python3
import logging
import requests
import argparse



def get_device_data(device_id, slnet_token):
    """
    Получение полной информации о состоянии устройства
    :param device_id: device_id
    :param slnet_token: StarLineAPI Token
    :return: Код, необходимый для получения токена приложения
    """
    url = "https://developer.starline.ru/json/v3/device/{}/data".format(device_id)
    logging.info('execute request: {}'.format(url))
    cookies = "slnet={}".format(slnet_token)

    r = requests.get(url, headers={"Cookie": "slnet=" + slnet_token})
    response = r.json()
    logging.info('cookies: {}'.format(cookies))
    logging.info('response info: {}'.format(response))
    return response


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--deviceId", dest="deviceId", help="device id", default="", required=True)
    parser.add_argument("-s", "--slnetToken", dest="slnetToken", help="StarLineAPI Token", default="", required=True)
    args = parser.parse_args()
    logging.info('userId {}, slnetToken: {}'.format(args.userId, args.slnetToken))
    return args


def main():
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    args = get_args()
    get_device_data(args.userId, args.slnetToken)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(e)