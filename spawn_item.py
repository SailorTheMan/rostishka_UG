import requests
import json
import sqlite3
from sqlite3 import Error
import time, datetime

import FactoryController as fio

SIM_ADDRESS = 'http://loopback:7410'    #my VM address
START_TIME = time.time()
WAIT_ITEM_RFID = False
LAST_RFID = None

def select_item(conn, priority):
    cur = conn.cursor()
    cur.execute("SELECT * FROM id_factory WHERE ID=?", (priority,))

    rows = cur.fetchall()

    for row in rows:
        print(row)
    
    return rows

def time_to_sec(cur_time):
    ten = time.strptime('10:00:00', "%H:%M:%S")
    ten = datetime.timedelta(hours=ten.tm_hour, minutes=ten.tm_min, seconds=ten.tm_sec).seconds
    sec = time.strptime(cur_time, "%H:%M:%S")
    sec = datetime.timedelta(hours=sec.tm_hour, minutes=sec.tm_min, seconds=sec.tm_sec).seconds
    return sec-ten

def find_panding_items(conn):
    
    for row in conn.execute('SELECT * FROM id_factory ORDER BY "Time in"'):
        cur_time = time.time() - START_TIME
        # if time to be in sim but not in sim
        
        if (cur_time > time_to_sec(row[4]) and cur_time < time_to_sec(row[5])):
            if (not(row[8])):
                print(row)
                return row
        return None


def get_RFID():
    # делаю прямыми сетами и гетами потому что тут нужно сразу получить реакцию
    rfid_command.set_value('1')
    rfid_iec.set_value(True)
    stat = rfid_stat.get_value()
    print(stat)
    rfid_iec.set_value(False)
    if (stat == 0):
        value = rfid_iread.get_value()
        return value
    else:
        return None 


def spawn_item(item):
    global LAST_RFID
    global WAIT_ITEM_RFID
    em1_emit.value = 'false'
    # conn to db
    conn = sqlite3.connect('sim_data.sqlite')
    cursor = conn.cursor()
    # TODO spawn item in sim, добавть ожидание рфид датчика и добавление рфид метки 
    if (not(WAIT_ITEM_RFID)):
        em1_part.value = 8192
        em1_emit.value = "true"
        WAIT_ITEM_RFID = True
        # TODO возможно тут надо как то по разумистки включать конвейер но пока так
        rc_input.value = 'true'

    RFID_value = get_RFID()
    if LAST_RFID == RFID_value:
        RFID_value = None

    if RFID_value is not None:
        cursor.execute("UPDATE id_factory SET in_sim=1 WHERE ID=?;", (item[2], ))
        conn.commit()
        cursor.execute("UPDATE id_factory SET RFID_ID=? WHERE ID=?;", (RFID_value,item[2], ))
        conn.commit()
        WAIT_ITEM_RFID = False
        rc_input.value = 'false'
        print(f'{item[2]} in sim, in_sim: {item[7]}')
        LAST_RFID = RFID_value
    
    
    
        

def loop():
    
    controller.fetch_tags()
    print(time.time() - START_TIME)
    # conn to db
    conn = sqlite3.connect('sim_data.sqlite')
    cursor = conn.cursor()
    # debag 
    cursor.execute("UPDATE id_factory SET in_sim=0")
    conn.commit()
    ## check pending DB entries
    item = find_panding_items(conn)
    if (item is not None):
        spawn_item(item)
        item = None
    
    ## start conveyor after fresh spawn
    

    ## arm scanner after fresh cargo spawn
    #if cargo_spawned_recently > 0:
    

    ##   RFID read entrance
    



    ## Entrance scanner routine
    
    

    controller.push_tags()



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
    ## RFID ON ENTRANCE
    rfid_command = controller.attach_tag("RFID In Command")
    rfid_iec = controller.attach_tag("RFID In Execute Command")
    rfid_iread = controller.attach_tag("RFID In Read Data")
    rfid_stat = controller.attach_tag("RFID In Status")
    
    # debag 
    conn = sqlite3.connect('sim_data.sqlite')
    cursor = conn.cursor()
    cursor.execute("UPDATE id_factory SET in_sim=0")
    conn.commit()
    conn.close()
    
    # controller.sim_start()     doesnt work as expected

    ## 'global' variables
    # cargo_spawned_recently = 0

    # cargo_dict = {}

    ## end global

    # em1_part.set_value(8192)
    # em1_emit.set_value("true")
    # time.sleep(1)
    # em1_part.set_value(8192)
    # em1_emit.set_value("false")
    # cargo_spawned_recently += 1

    while(True):
        loop()