import requests
import json
import sqlite3
from sqlite3 import Error
import time

import FactoryController as fio

SIM_ADDRESS = 'http://192.168.220.129:7410'    #my VM address



def loop():
    controller.fetch_tags()
    global cargo_spawned_recently
    ## check pending DB entries

    
    ## start conveyor after fresh spawn
    if cargo_spawned_recently > 0:
        rc_input.value = True

    ## arm scanner after fresh cargo spawn
    if cargo_spawned_recently > 0:
        rfid_command.value = 1
        rfid_iec.value = 'true'

    ##   RFID read entrance
    rfid_data = rfid_iread.value
    rfid_error = rfid_stat.value

    if (rfid_error == 0):
        print(rfid_data)
        #cargo_dict[rfid_data]          ## probably Cargo class needed
    elif (rfid_error == 1):
        print("Error No Tag")
    elif (rfid_error == 2):
        print("Error Too Many Tags")
    else:
        print('Another Error')
    rfid_iec.value = 'true'

    ## Entrance scanner routine
    if rs1_in.value == False:
        cargo_spawned_recently -= 1
        rc_input.value = False



    

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
    
    
   
    
    
    # controller.sim_start()     doesnt work as expected

    ## 'global' variables
    cargo_spawned_recently = 0

    cargo_dict = {}

    ## end global

    em1_part.set_value(8192)
    em1_emit.set_value("true")
    time.sleep(1)
    em1_part.set_value(8192)
    em1_emit.set_value("false")
    cargo_spawned_recently += 1

    while(True):
        loop()
    