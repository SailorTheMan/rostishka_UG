import requests
import json
import sqlite3
from sqlite3 import Error
import time




def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def spam_stackable_box():
    payload = [
    {
        "name": "Emitter 1 (Part)",
        "value": 8192
    },
    {
        "name": "Emitter 1 (Emit)",
        "value": "true"
    },
    ]

    requests.put('http://127.0.0.1:7410/api/tag/values/by-name', json=payload)
    time.sleep(1)
    payload = [
    {
        "name": "Emitter 1 (Part)",
        "value": 8192
    },
    {
        "name": "Emitter 1 (Emit)",
        "value": "false"
    },
    ]

    requests.put('http://127.0.0.1:7410/api/tag/values/by-name', json=payload)
  

def add_new_RFID():
    payload = [
    {
        "name": "RFID In Command",
        "value": 1
    },
    {
        "name": "RFID In Execute Command",
        "value": "true"
    },
    ]

    requests.put('http://127.0.0.1:7410/api/tag/values/by-name', json=payload)
    time.sleep(1)
    rfid_data = requests.get('http://127.0.0.1:7410/api/tags/by-name/RFID In Read Data')
    rfid_error = requests.get('http://127.0.0.1:7410/api/tags/by-name/RFID In Status')
    
    if (rfid_error.json()[0]['value'] == 0):
        print(rfid_data.json()[0]['value'])
    elif (rfid_error.json()[0]['value'] == 1):
        print("Error No Tag")
    elif (rfid_error.json()[0]['value'] == 2):
        print("Error Too Many Tags")
    else:
        print('other Error')

    payload = [
    {
        "name": "RFID In Execute Command",
        "value": "false"
    },
    ]
    requests.put('http://127.0.0.1:7410/api/tag/values/by-name', json=payload)


def wait_first_rs():
    # Start conveyor (RC (4m) 1.1), wait item on "RS 1 In" laser sensor and stop conveyor

    payload = [
    {
        "name": "RC (4m) 1.1",
        "value": "true"
    },
    ]
    requests.put('http://127.0.0.1:7410/api/tag/values/by-name', json=payload)
    while(True):
        rs_status = requests.get('http://127.0.0.1:7410/api/tags/by-name/RS 1 In')
        if (rs_status.json()[0]['value'] != True):
            payload = [
            {
                "name": "RC (4m) 1.1",
                "value": "false"
            },
            ]
            requests.put('http://127.0.0.1:7410/api/tag/values/by-name', json=payload)
            break


def item_to_first_crane():
    """ 
    Deliver from first RFID to first crane
    StopR 1 Out - true
    CT 1 (+) - true
    RC (4m) 1.1 - true
    CT 1 Left - true
    CT 1A Right - true
    if RS 1A Out == False:
        StopR 1 Out - true
        CT 1 (+) - false
        RC (4m) 1.1 - false
        CT 1 Left - false
    RC A1 - true
    Curved RC A2 - true
    RC A3 - true 
    Load RC A4 - true 
    if At Load A == False :
        RC A1 - false
        Curved RC A2 - false
        RC A3 - false 
        Load RC A4 - false 
    """
    payload = [
    {
        "name": "StopR 1 Out",
        "value": "true"
    },
    {
        "name": "CT 1 (+)",
        "value": "true"
    },
    {
        "name": "RC (4m) 1.1",
        "value": "true"
    },
    ]
    requests.put('http://127.0.0.1:7410/api/tag/values/by-name', json=payload)
    time.sleep(2)
    payload = [
    {
        "name": "CT 1 (+)",
        "value": "false"
    },
    {
        "name": "RC (4m) 1.1",
        "value": "false"
    },
    {
        "name": "CT 1 Left",
        "value": "true"
    },
    {
        "name": "CT 1A Right",
        "value": "true"
    },
    ]
    requests.put('http://127.0.0.1:7410/api/tag/values/by-name', json=payload)
    while (True):
        rs_1a_status = requests.get('http://127.0.0.1:7410/api/tags/by-name/RS 1A Out')
        if (rs_1a_status.json()[0]['value'] != True):
            payload = [
            {
                "name": "StopR 1 Out",
                "value": "false"
            },
            {
                "name": "CT 1 (+)",
                "value": "false"
            },
            {
                "name": "RC (4m) 1.1",
                "value": "false"
            },
            {
                "name": "CT 1 Left",
                "value": "false"
            },
            ]
            requests.put('http://127.0.0.1:7410/api/tag/values/by-name', json=payload)
            break
    payload = [
    {
        "name": "RC A1",
        "value": "true"
    },
    {
        "name": "Curved RC A2",
        "value": "true"
    },
    {
        "name": "RC A3",
        "value": "true"
    },
    {
        "name": "Load RC A4",
        "value": "true"
    },
    ]
    requests.put('http://127.0.0.1:7410/api/tag/values/by-name', json=payload)
    while (True):
        at_load_a_status = requests.get('http://127.0.0.1:7410/api/tags/by-name/At Load A')
        if (at_load_a_status.json()[0]['value'] != True):
            payload = [
            {
                "name": "RC A1",
                "value": "false"
            },
            {
                "name": "Curved RC A2",
                "value": "false"
            },
            {
                "name": "RC A3",
                "value": "false"
            },
            {
                "name": "Load RC A4",
                "value": "false"
            },
            {
                "name": "CT 1A Right",
                "value": "false"
            },
            ]
            requests.put('http://127.0.0.1:7410/api/tag/values/by-name', json=payload)
            break




# create_connection("C:\\nti_ug_test\\test.db")
spam_stackable_box()
wait_first_rs()
add_new_RFID()

item_to_first_crane()