#!/.venv/Scripts/python.exe

import requests
import json
import sqlite3
from sqlite3 import Error
import time
import asyncio

import FactoryController as fio

SIM_ADDRESS = 'http://192.168.220.129:7410'    #my local VM address




async def pallet1():
    #await asyncio.gather(RC10.move(), RC1.move(), RCa1.move(), RCCa2.move(), RCa3.move(), lRCa4.move())
    await RC1.move()
    await asyncio.gather(RC1.transit_next(), CT1.accept_to('forward'))
    await asyncio.gather(CT1.move_to('left'), CT1A.accept_to('right'))
    await CT1A.move_to('right')
    await Arc1.move()

async def pallet2():
    
    await CT1A.move_to('right')
    await Arc1.move()

### WOW 
async def task_controll():
    await asyncio.gather(pallet1(), pallet2())
    #await pallet1()
    #await pallet2()





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

    ## CONVEYOR SERIES
    Arc1 = fio.Conv_Series(al_a, rc_a1, rcc_a2, rc_a3, l_rc_a4)

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
    asyncio.run( task_controll() ) 
    #asyncio.run(loop())
        #pass
        
    