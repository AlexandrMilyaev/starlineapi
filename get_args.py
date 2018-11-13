#!/usr/bin/python3
import logging
import argparse

__author__ = "Kosterev Grigoriy <kosterev@starline.ru>"
__date__ = "13.10.2018"

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--appId", dest="appId", help="application identification", default="", required=True)
    parser.add_argument("-c", "--appCode", dest="appCode", help="application code", default="", required=True)
    parser.add_argument("-l", "--login", dest="login", help="account login", default="", required=True)
    parser.add_argument("-p", "--password", dest="password", help="account password", default="", required=True)
    args = parser.parse_args()
    logging.info("appId: {}, appCode: {}, login: {}, password: {}".format(args.appId, args.appCode, args.login, args.password))

