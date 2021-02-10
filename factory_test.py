import requests
import json
import sqlite3
from sqlite3 import Error
import time


import FactoryController as fio

SIM_ADDRESS = 'http://192.168.220.129:7410'    #my VM address

def spawn_stackable_box():
    em1_part.set_value(8192)
    em1_emit.set_value("true")

    time.sleep(1)

    em1_part.set_value(8192)
    em1_emit.set_value("false")


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

    rc_input.set_value("true")

    while(True):

        rs_status = rs1_in.get_value()
        if (rs_status != True):
            rc_input.set_value("false")
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
    controller.batch_write(payload)

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

    controller.batch_write(payload)            ### requests.put('http://127.0.0.1:7410/api/tag/values/by-name', json=payload)

    while (True):
        rs_1a_status = rs1_out.get_value()
        if (rs_1a_status != True):
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
            controller.batch_write(payload)  
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
    controller.batch_write(payload)  

    while (True):
        at_load_a_status = al_a.get_value()
        if (at_load_a_status != True):
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
            controller.batch_write(payload)  
            break




# create_connection("C:\\nti_ug_test\\test.db")
if __name__ == '__main__':
    controller = fio.FIO_Controller(SIM_ADDRESS)
    ##  Tag declaration
    print('Tag declaration')
    em1_part = controller.attach_tag('Emitter 1 (Part)')
    em1_emit = controller.attach_tag('Emitter 1 (Emit)')
    rc_input = controller.attach_tag('RC (4m) 1.1')
    rs1_in = controller.attach_tag('RS 1 In')
    rs1_out = controller.attach_tag('RS 1A Out')
    al_a = controller.attach_tag('At Load A')
    

    # controller.sim_start()     doesnt work as expected
    controller.fetch_tags()
    ##
    print('Spawn box')
    spawn_stackable_box()
    print('Wait conveyor')
    wait_first_rs()

    '''
    add_new_RFID()

    item_to_first_crane()
    '''