import requests
import json
import sqlite3
from sqlite3 import Error
import time
import asyncio

import FactoryController as fio

SIM_ADDRESS = 'http://192.168.220.129:7410'    #my VM address
    

async def ct1_handler():
    global entrance_rfid_read
    global CT1_positioning_completed

    #print('two')
    # crossing conveyor entrance
    ct1_plus.value = True
    stop_ct1 = True                 # BLOCKS THE RS1_Out !!!!
    if rs1_in.value == False:  # conveyot keeps on until line is clear
        pass#rc_input.value = True

    # crossing conveyor change direction condition
    if cs_1.value == True and rs1_in.value == True:
        #print('stop CC')
        ct1_plus.value = False
        #rc_input.value = False

        
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
        #print('four')
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
    
    asyncio.gather(rc10.move(), rc1.move())
    

    ## start conveyor after fresh spawn
    if cargo_spawned_recently > 0:

        
        data = rc1.read_rfid()

    ## Entrance scanner routine
    if entrance_rfid_read == True:
        await ct1_handler()
    
    await ct1_ct1a_transit()

    await ct1a_crane_transit()

    controller.push_tags()          ### <- updates tags in the end






### WOW 
async def wtf():
    #await asyncio.gather(RC10.move(), RC1.move(), RCa1.move(), RCCa2.move(), RCa3.move(), lRCa4.move())
    await RC1.move()
    await asyncio.gather(RC1.transit_next(), CT1.accept_to('forward'))
    await asyncio.gather(CT1.move_to('left'), CT1A.accept_to('right'))






if __name__ == '__main__':
    controller = fio.FIO_Controller(SIM_ADDRESS)
    #####       Tag declaration      #####
    print('Tag declaration')
    em1_part = controller.attach_tag('Emitter 1 (Part)')
    em1_emit = controller.attach_tag('Emitter 1 (Emit)')
    ## linear conveyor spawn 
    rc_input =  controller.attach_tag('RC (4m) 1.1')
    rs1_in =    controller.attach_tag('RS 1 In')
    ## RFID ON ENTRANCE
    rfid_command =  controller.attach_tag("RFID In Command")
    rfid_iec =      controller.attach_tag("RFID In Execute Command")
    rfid_iread =    controller.attach_tag("RFID In Read Data")
    rfid_stat =     controller.attach_tag("RFID In Status")
    ## crossing conveyor entrance
    ct1_plus =  controller.attach_tag("CT 1 (+)", tag_id='17862cd4-a781-4ee8-8f5b-12543abc0c12')
    ct1_min =   controller.attach_tag("CT 1 (-)", tag_id='54fd23dc-c971-4ce9-9561-46d223a0b786')
    ct1_left =  controller.attach_tag("CT 1 Left")
    ct1_right = controller.attach_tag("CT 1 Right")
    cs_1 =      controller.attach_tag("CS 1")
    stop_ct1 =  controller.attach_tag("StopR 1 Out")
    rs1_out  =  controller.attach_tag('RS 1 Out')
    ## crossing conveyor next to entrance one
    ct1a_plus =     controller.attach_tag("CT 1A (+)", tag_id='6ba24a7c-543c-4f84-bcb1-fc02ccc9078c')
    ct1a_min =      controller.attach_tag("CT 1A (-)", tag_id='f89666ca-4a6f-4af5-ac23-ba820d0b2597')
    ct1a_left =     controller.attach_tag("CT 1A Left") 
    ct1a_right =    controller.attach_tag("CT 1A Right")
    cs_1a =         controller.attach_tag("CS 1A")
    stop_ct1a =     controller.attach_tag("StopR 1A In")
    rs1a_out =      controller.attach_tag('RS 1A Out')
    ## Conveyors curve 1A - Crane 1
    rc_a1 =     controller.attach_tag('RC A1')
    rcc_a2 =    controller.attach_tag('Curved RC A2')
    rc_a3 =     controller.attach_tag('RC A3')
    ## First crane arrivals
    l_rc_a4 =   controller.attach_tag('Load RC A4')
    al_a =      controller.attach_tag('At Load A')
    ## test conveyor
    rc_test = controller.attach_tag('RC A10')
    rs1a_in = controller.attach_tag('RS 1A In')

    ##      CONVEYORS 
    RC1 =   fio.Conveyor(rc_input, rs1_in, (rfid_command, rfid_iec, rfid_iread, rfid_stat))
    RC10 =  fio.Conveyor(rc_test, rs1a_in)
    RCa1 =  fio.Conveyor(rc_a1, al_a)
    RCCa2 = fio.Conveyor(rcc_a2, al_a)  # arc start
    RCa3 =  fio.Conveyor(rc_a3, al_a)
    lRCa4 = fio.Conveyor(l_rc_a4, al_a) # arc end

    ##      CROSSING CONVEYORS
    CT1 =   fio.Crossing_conveyor(ct1_plus, ct1_min, ct1_left, ct1_right, cs_1, rs1_out, stop_ct1, wait_time=2.1)
    CT1A =  fio.Crossing_conveyor(ct1a_plus, ct1a_min, ct1a_left, ct1a_right, cs_1a, rs1a_out, stop_ct1a, wait_time=3.5)

    #####   END DECLARATION   #####

    # controller.sim_start()     doesnt work as expected
    controller.fetch_tags()


    em1_part.set_value(8192)
    #em1_emit.set_value("true")
    time.sleep(1)
    em1_part.set_value(8192)
    em1_emit.set_value("false")

    #loop = asyncio.get_event_loop()  
    #asyncio.ensure_future(rc10.move())
    #asyncio.ensure_future(rc1.move())



    #while(True):
    asyncio.run(wtf() ) 
    #asyncio.run(loop())
        #pass
        
    