import requests
import json
from time import sleep
from datetime import datetime, timedelta
from sys import exit


CREDS_FILE_PATH="./creds.json"
ITEM_ID="298097256"

DEBUG=True


def read_creds_file():
    with open(CREDS_FILE_PATH,'r') as creds_json:
        auth = json.load(creds_json)
        return auth


def cibus_login(sess):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'he',
        'application-id': 'E5D5FEF5-A05E-4C64-AEBA-BA0CECA0E402',
        'cache-control': 'no-cache',
        'content-type': 'application/json; charset=UTF-8',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://consumers.pluxee.co.il/',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    }

    auth = read_creds_file()

    json_data = {
        'username': auth['username'],
        'password': auth['password'],
        'company': '',
    }

    # Setting the semi-static headers to persist
    sess.headers.update(headers)

    response = sess.post("https://api.capir.pluxee.co.il/auth/authToken", headers=headers, json=json_data)
    # Code 201 means a token has been successfully created
    if response.status_code != 201:
        print(f"Issue logging in, response: {response.text}")

    if DEBUG:
        print('\ncibus_login\n')
        print(response.text)

    return sess


def add_item_to_cart(sess):
    json_data = {
        'type': 'prx_add_prod_to_cart',
        'deal_id': ITEM_ID,
    }
    print (sess.cookies.get('token'))
    response = sess.post('https://api.consumers.pluxee.co.il/api/main.py', json=json_data)

    if DEBUG:
        print('\nadd_item_to_cart\n')
        print(response.text)


def time_str_for_purchase():
    minutes = (datetime.now() + timedelta(minutes=15)//15*15).minute
    #minutes should be the next 15 min interval 
    hours = (datetime.now().hour)
    #if the time is 23:12 the time sent should be 23:15
    return f'{str(hours)}:{str(minutes)}'

def simulate_purchase(sess):
    json_data = {
        'order_time': time_str_for_purchase(),
        'type': 'prx_simulate_order',
    }

    response = sess.post('https://api.consumers.pluxee.co.il/api/main.py', json=json_data)

    if DEBUG:
        print('\nsubmit_purchase\n')
        print(response.text)


def complete_purchase(sess):
    json_data = {
        'order_time': time_str_for_purchase(),
        'type': 'prx_apply_order',
    }

    response = sess.post('https://api.consumers.pluxee.co.il/api/main.py', json=json_data)

    if DEBUG:
        print('\ncomplete_purchase\n')
        print(response.text)


def main():
    sess = requests.Session()
    cibus_login(sess)
    sleep(2)
    #wait due to "token not found" response from cibus server if runs too quickly
    add_item_to_cart(sess)
    simulate_purchase(sess)
    #complete_purchase(sess)
    #only enable this last function if you would like to complete the purchase


if __name__ == "__main__":
    main()

