# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 20:25:29 2024

@author: ashwe
"""
import sys

def get_keys():
    config_path = 'config/'
    key_file = config_path + "key.txt"
    try:
        key_secret = open(key_file, "r").read().split()
    except FileNotFoundError:
        key_secret = []
        key_secret.append(input("Enter API Key\n"))
        key_secret.append(input("Enter API Secret\n"))
        key_secret.append(input("Enter Client ID/Username\n"))
        key_secret.append(input("Enter Password/PIN\n"))
        key_secret.append(input("Enter TOTP String\n"))

        with open(key_file, "w") as f:
            for key in key_secret:
                    f.write(f'{key}\n')
            f.flush()
            f.close()

    return key_secret

API_KEY = get_keys()[0]
API_SECRET = get_keys()[1]
CLIENT_ID = get_keys()[2]
PASSWORD = get_keys()[3]
TOTP_TOKEN = get_keys()[4]
