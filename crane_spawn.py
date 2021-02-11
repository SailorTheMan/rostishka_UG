import requests
import json
from time import sleep
import time, datetime
import asyncio
import sqlite3

import FactoryController as fio

SIM_ADDRESS = 'http://127.0.0.1:7410'    #my VM address



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
                # print(row)
                return row
    return None


async def get_RFID():
    # делаю прямыми сетами и гетами потому что тут нужно сразу получить реакцию
    rfid_command.set_value('1')
    rfid_iec.set_value(True)
    await asyncio.sleep(0.1)
    stat = rfid_stat.get_value()
    # print(stat)
    rfid_iec.set_value(False)
    if (stat == 0):
        value = rfid_iread.get_value()
        return value
    else:
        return None 


async def spawn_item(item):
    # TODO добавить условие ожидание ошибки 1 (ожидать пока коробка уедет из зоны действия рфид датчика)
    global LAST_RFID
    global WAIT_ITEM_RFID
    em1_emit.value = 'false'
    # conn to db
    conn = sqlite3.connect('sim_data.sqlite')
    cursor = conn.cursor()
    
    RFID_value = await get_RFID()
    if LAST_RFID == RFID_value:
        RFID_value = None

    if (not(WAIT_ITEM_RFID) and rfid_stat.value == 1):
        em1_part.value = 8192
        em1_emit.value = "true"
        WAIT_ITEM_RFID = True
        # TODO возможно тут надо как то по разумистки включать конвейер но пока так
        rc_input.value = 'true'
    

    if RFID_value is not None:
        cursor.execute("UPDATE id_factory SET in_sim=1 WHERE ID=?;", (item[2], ))
        conn.commit()
        cursor.execute("UPDATE id_factory SET RFID_ID=? WHERE ID=?;", (RFID_value,item[2], ))
        conn.commit()
        WAIT_ITEM_RFID = False
        # rc_input.value = 'false'
        print(f'{item[2]} in sim, in_sim: {item[7]}')
        LAST_RFID = RFID_value

    conn.close()
    
  


async def item_to_shelf_A(number):
    
    fork_left_a.set_value(True)
    while(not(at_left_a.get_value())): await asyncio.sleep(0.1)
   
    lift_a.set_value(True)
    await asyncio.sleep(0.1)
    while(not(mov_z_a.get_value())): await asyncio.sleep(0.1)

 
    fork_left_a.set_value(False)
    while(not((at_mid_a.get_value()))): await asyncio.sleep(0.1)

    
    targ_pos_a.set_value(number)
    await asyncio.sleep(0.1)
    while (mov_z_a.get_value() or mov_x_a.get_value()): await asyncio.sleep(0.1)
    
    fork_left_a.set_value(True)
    while(not(at_left_a.get_value())): await asyncio.sleep(0.1)
   
    lift_a.set_value(False)
    await asyncio.sleep(0.1)
    while(mov_z_a.get_value()): await asyncio.sleep(0.1)
    
    fork_left_a.set_value(False)
    while(not(at_mid_a.get_value())): await asyncio.sleep(0.1)
    
    targ_pos_a.set_value(55)
    await asyncio.sleep(0.1)
    while(mov_z_a.get_value()) or mov_x_a.get_value(): await asyncio.sleep(0.1)


async def item_to_shelf_B(number):
    
    fork_left_b.set_value(True)
    while(not(at_left_b.get_value())): await asyncio.sleep(0.1)
   
    lift_b.set_value(True)
    await asyncio.sleep(0.1)
    while(not(mov_z_b.get_value())): await asyncio.sleep(0.1)

 
    fork_left_b.set_value(False)
    while(not((at_mid_b.get_value()))): await asyncio.sleep(0.1)

    
    targ_pos_b.set_value(number)
    await asyncio.sleep(0.1)
    while (mov_z_b.get_value() or mov_x_b.get_value()): await asyncio.sleep(0.1)
    
    fork_left_b.set_value(True)
    while(not(at_left_b.get_value())): await asyncio.sleep(0.1)
   
    lift_b.set_value(False)
    await asyncio.sleep(0.1)
    while(mov_z_b.get_value()): await asyncio.sleep(0.1)
    
    fork_left_b.set_value(False)
    while(not(at_mid_b.get_value())): await asyncio.sleep(0.1)
    
    targ_pos_b.set_value(55)
    await asyncio.sleep(0.1)
    while(mov_z_b.get_value()) or mov_x_b.get_value(): await asyncio.sleep(0.1)


async def item_from_shelf_A(number):
    
    targ_pos_a.set_value(number)
    await asyncio.sleep(0.1)
    while (mov_z_a.get_value() or mov_x_a.get_value()): await asyncio.sleep(0.1)


    fork_left_a.set_value(True)
    while(not(at_left_a.get_value())): await asyncio.sleep(0.1)
   
    lift_a.set_value(True)
    await asyncio.sleep(0.1)
    while(not(mov_z_a.get_value())): await asyncio.sleep(0.1)

 
    fork_left_a.set_value(False)
    while(not((at_mid_a.get_value()))): await asyncio.sleep(0.1)

    targ_pos_a.set_value(55)
    await asyncio.sleep(0.1)
    while(mov_z_a.get_value()) or mov_x_a.get_value(): await asyncio.sleep(0.1)
    
    
    fork_right_a.set_value(True)
    while(not(at_right_a.get_value())): await asyncio.sleep(0.1)
   
    lift_a.set_value(False)
    await asyncio.sleep(0.1)
    while(mov_z_a.get_value()): await asyncio.sleep(0.1)
    
    fork_right_a.set_value(False)
    while(not(at_mid_a.get_value())): await asyncio.sleep(0.1)
    

async def item_from_shelf_B(number):
    
    targ_pos_b.set_value(number)
    await asyncio.sleep(0.1)
    while (mov_z_b.get_value() or mov_x_b.get_value()): await asyncio.sleep(0.1)

    fork_left_b.set_value(True)
    while(not(at_left_b.get_value())): await asyncio.sleep(0.1)
   
    lift_b.set_value(True)
    await asyncio.sleep(0.1)
    while(not(mov_z_b.get_value())): await asyncio.sleep(0.1)

 
    fork_left_b.set_value(False)
    while(not((at_mid_b.get_value()))): await asyncio.sleep(0.1)

    targ_pos_b.set_value(55)
    await asyncio.sleep(0.1)
    while(mov_z_b.get_value()) or mov_x_b.get_value(): await asyncio.sleep(0.1)

    
    fork_right_b.set_value(True)
    while(not(at_right_b.get_value())): await asyncio.sleep(0.1)
   
    lift_b.set_value(False)
    await asyncio.sleep(0.1)
    while(mov_z_b.get_value()): await asyncio.sleep(0.1)
    
    fork_right_b.set_value(False)
    while(not(at_mid_b.get_value())): await asyncio.sleep(0.1)
    

async def task_controll():
    while(True):
        # controller.fetch_tags()
        # print(time.time() - START_TIME)
        # # conn to db
        # conn = sqlite3.connect('sim_data.sqlite')
        # cursor = conn.cursor()

        # ## check pending DB entries
        # item = find_panding_items(conn)
        # if (item is not None):
        #     await spawn_item(item)
        #     item = None
        

        # ## crane work

        await asyncio.gather(item_to_shelf_A(15), item_to_shelf_B(29))
        
        await asyncio.gather(item_from_shelf_A(15), item_from_shelf_B(29))

        ## start conveyor after fresh spawn
        

        ## arm scanner after fresh cargo spawn
        #if cargo_spawned_recently > 0:
        

        ##   RFID read entrance
        



        ## Entrance scanner routine
        
        
        # conn.close()
        # controller.push_tags()


        





if __name__ == '__main__':
    controller = fio.FIO_Controller(SIM_ADDRESS)
    ##  Tag declaration
    print('Tag declaration')

    ## emmiter and input conveyer
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

    ## cranes
    mov_x_a = controller.attach_tag('Moving X A')
    mov_z_a = controller.attach_tag('Moving Z A')
    targ_pos_a = controller.attach_tag('Target Position A')
    at_mid_a = controller.attach_tag('At Middle A')
    at_left_a = controller.attach_tag('At Left A')
    at_right_a = controller.attach_tag('At Right A')
    fork_left_a = controller.attach_tag('Forks Left A')
    fork_right_a = controller.attach_tag('Forks Right A')
    lift_a = controller.attach_tag('Lift A')
    mov_x_b = controller.attach_tag('Moving X B')
    mov_z_b = controller.attach_tag('Moving Z B')
    targ_pos_b = controller.attach_tag('Target Position B')
    at_mid_b = controller.attach_tag('At Middle B')
    at_left_b = controller.attach_tag('At Left B')
    at_right_b = controller.attach_tag('At Right B')
    fork_left_b = controller.attach_tag('Forks Left B')
    fork_right_b = controller.attach_tag('Forks Right B')
    lift_b = controller.attach_tag('Lift B')

    # debag - resert db 
    conn = sqlite3.connect('sim_data.sqlite')
    cursor = conn.cursor()
    cursor.execute("UPDATE id_factory SET in_sim=0")
    conn.commit()
    conn.close()
    
       
    asyncio.run( task_controll() )

