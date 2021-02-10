import requests
import json
import sqlite3
from sqlite3 import Error
import time
import asyncio

import FactoryController as fio

SIM_ADDRESS = 'http://192.168.220.129:7410'    #my VM address

async def welcome():
    global entrance_rfid_read
    print('one')
    rc_input.value = True

    if rs1_in.value == False:
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

async def ct1_handler():
    global entrance_rfid_read
    global CT1_positioning_completed

    #print('two')
    # crossing conveyor entrance
    ct1_plus.value = True
    stop_ct1 = True                 # BLOCKS THE RS1_Out !!!!
    if rs1_in.value == False:  # conveyot keeps on until line is clear
        rc_input.value = True

    # crossing conveyor change direction condition
    if cs_1.value == True and rs1_in.value == True:
        #print('stop CC')
        ct1_plus.value = False
        rc_input.value = False

        
        entrance_rfid_read = False
        CT1_positioning_completed = True

async def ct1_ct1a_transit():
    global CT1_positioning_completed
    #print('three')

    if cs_1.value == True and CT1_positioning_completed == True:
        ct1_left.value = True
        ct1a_right.value = True
    if cs_1a.value == True:
        ct1_left.value = False
        rc_a1.value = True
        CT1_positioning_completed = False

async def ct1a_crane_transit():
        print('four')
        if rs1a_out.value == False and cs_1a.value == False:
            
            ct1a_right.value = False
            rcc_a2.value = True
            rc_a3.value = True



async def loop():
    controller.fetch_tags()         ### <- updates tags in the beginnig

    global cargo_spawned_recently
    global entrance_rfid_read
    global CT1_positioning_completed
    global CT1A_positioning_completed
    global CT1_CT1A_transit_process
    ## check pending DB entries

    CT1_CT1A_transit_process = True
    
    ## start conveyor after fresh spawn
    if cargo_spawned_recently > 0:
        await welcome()

    ## Entrance scanner routine
    if entrance_rfid_read == True:
        await ct1_handler()
    
    await ct1_ct1a_transit()

    await ct1a_crane_transit()

    controller.push_tags()          ### <- updates tags in the end







if __name__ == '__main__':
    controller = fio.FIO_Controller(SIM_ADDRESS)
    ##  Tag declaration
    print('Tag declaration')
    em1_part = controller.attach_tag('Emitter 1 (Part)')
    em1_emit = controller.attach_tag('Emitter 1 (Emit)')
    ## linear conveyor spawn 
    rc_input = controller.attach_tag('RC (4m) 1.1')
    rs1_in = controller.attach_tag('RS 1 In')
    ## RFID ON ENTRANCE
    rfid_command = controller.attach_tag("RFID In Command")
    rfid_iec = controller.attach_tag("RFID In Execute Command")
    rfid_iread = controller.attach_tag("RFID In Read Data")
    rfid_stat = controller.attach_tag("RFID In Status")
    ##
    rc1 = fio.Conveyor(rc_input, rs1_in, (rfid_command, rfid_iec, rfid_iread, rfid_stat))
    ## crossing conveyor entrance
    ct1_plus = controller.attach_tag("CT 1 (+)", tag_id='17862cd4-a781-4ee8-8f5b-12543abc0c12')
    ct1_left = controller.attach_tag("CT 1 Left")
    cs_1 = controller.attach_tag("CS 1")
    stop_ct1 = controller.attach_tag("StopR 1 Out")
    ## crossing conveyor next to entrance one
    ct1a_right = controller.attach_tag("CT 1A Right")
    cs_1a = controller.attach_tag("CS 1A")
    
    rs1a_out = controller.attach_tag('RS 1A Out')
    ## Conveyors curve 1A - Crane 1
    rc_a1 = controller.attach_tag('RC A1')
    rcc_a2 = controller.attach_tag('Curved RC A2')
    rc_a3 = controller.attach_tag('RC A3')
    ## First crane arrivals
    l_rc_a4 = controller.attach_tag('Load RC A4')
    al_a = controller.attach_tag('At Load A')

    
    # controller.sim_start()     doesnt work as expected

    ## 'global' variables
    cargo_spawned_recently = 0
    CT1_positioning_completed = False
    CT1A_positioning_completed = False
    CT1_CT1A_transit_process = False
    entrance_rfid_read = False

    cargo_dict = {}

    ## end global

    em1_part.set_value(8192)
    #em1_emit.set_value("true")
    time.sleep(1)
    em1_part.set_value(8192)
    em1_emit.set_value("false")
    cargo_spawned_recently += 1


    while(True):
        
        asyncio.run(loop())
        
    