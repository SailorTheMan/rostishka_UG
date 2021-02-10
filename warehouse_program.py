import requests
import json
import sqlite3
from sqlite3 import Error
import time

import FactoryController as fio

SIM_ADDRESS = 'http://192.168.220.129:7410'    #my VM address



def loop():
    global cargo_spawned_recently
    global entrance_rfid_read
    ## check pending DB entries


    
    ## start conveyor after fresh spawn
    if cargo_spawned_recently > 0:
        rc_input.value = True


    ## Entrance scanner routine
    rfid_data = -1
    if rs1_in.value == False and entrance_rfid_read == False:
        cargo_spawned_recently -= 1
        # Stop conveyor
        rc_input.value = False
        # RFID read on entrance 
        rfid_command.value = 1
        rfid_iec.value = 'true'
        
        rfid_data = rfid_iread.value
        rfid_error = rfid_stat.value

        if (rfid_error == 0):
            print(rfid_data)
            entrance_rfid_read = True
            #cargo_dict[rfid_data]          ## probably Cargo class needed
        elif (rfid_error == 1):
            print("Error No Tag")
        elif (rfid_error == 2):
            print("Error Too Many Tags")
        else:
            print('Another Error')
        rfid_iec.value = 'true'
    
    # crossing conveyor entrance
    if entrance_rfid_read == True:
        ct1_plus.value = True
        if rs1_in.value == False:
            rc_input.value = True
        

    # crossing conveyor 
    if cs_1.value == True:
        print('stop CC')
        ct1_plus.value = False
        rc_input.value = False

    

    

    



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
    ## crossing conveyor entrance
    ct1_plus = controller.attach_tag("CT 1 (+)", tag_id='17862cd4-a781-4ee8-8f5b-12543abc0c12')
    ct1_plus.set_value(True)
    cs_1 = controller.attach_tag("CS 1")
    
   
    
    
    # controller.sim_start()     doesnt work as expected

    ## 'global' variables
    cargo_spawned_recently = 0
    entrance_rfid_read = False

    cargo_dict = {}

    ## end global

    em1_part.set_value(8192)
    em1_emit.set_value("true")
    time.sleep(1)
    em1_part.set_value(8192)
    em1_emit.set_value("false")
    cargo_spawned_recently += 1


    while(True):
        controller.fetch_tags()         ### <- updates tags in the beginnig
        loop()
        controller.push_tags()          ### <- updates tags in the end
    