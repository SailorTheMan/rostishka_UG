import requests
import json
import sqlite3
from sqlite3 import Error
import time

import FactoryController as fio

SIM_ADDRESS = 'http://192.168.220.129:7410'    #my VM address



def loop():
    controller.fetch_tags()

    ## check pending DB entries
        # spawn new box
        cargo_spawned = True

    



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
    rfid_ic = controller.attach_tag("RFID In Command")
    rfid_iec = controller.attach_tag("RFID In Execute Command")
   
    
    
    # controller.sim_start()     doesnt work as expected

    ## 'global' variables
    cargo_spawned = False

    loop()
    