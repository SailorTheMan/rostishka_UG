#!/.venv/Scripts/python.exe

import requests
import json
import sqlite3
from sqlite3 import Error
import time, datetime
import asyncio

#from spawn_item import select_item, time_to_sec, find_pending_items, get_RFID, spawn__item
import FactoryController as fio
import cargo

SIM_ADDRESS = 'http://loopback:7410'    #my local VM address

#region spawn_item functions

START_TIME = time.time()
WAIT_ITEM_RFID = False
LAST_RFID = None
FREE_CELL = []
for i in range(216): FREE_CELL.append(i+1)



def time_to_sec(cur_time):
    ten = time.strptime('10:00:00', "%H:%M:%S")
    ten = datetime.timedelta(hours=ten.tm_hour, minutes=ten.tm_min, seconds=ten.tm_sec).seconds
    sec = time.strptime(cur_time, "%H:%M:%S")
    sec = datetime.timedelta(hours=sec.tm_hour, minutes=sec.tm_min, seconds=sec.tm_sec).seconds
    return sec-ten

def find_pending_items(conn):
    
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
    rfid_command.set_value(1)
    rfid_iec.set_value(True)
    time.sleep(0.1)
    stat = rfid_stat.get_value()
    print(stat)
    rfid_iec.set_value(False)
    if (stat == 0):
        value = rfid_iread.get_value()
        return value
    else:
        return None 


def spawn__item(item):
    # TODO добавить условие ожидание ошибки 1 (ожидать пока коробка уедет из зоны действия рфид датчика)
    global LAST_RFID
    global WAIT_ITEM_RFID
    em1_emit.set_value('false')
    # conn to db
    conn = sqlite3.connect('sim_data.sqlite')
    cursor = conn.cursor()
    
    RFID_value = get_RFID()
    if LAST_RFID == RFID_value:
        RFID_value = None

    if (not(WAIT_ITEM_RFID) and rfid_stat.value == 1):
        em1_part.set_value(8192)
        em1_emit.set_value("true")
        WAIT_ITEM_RFID = True
        rc_input.set_value('true')
    

    if RFID_value is not None:
        # новый объект приехал к рфид 
        cursor.execute("UPDATE id_factory SET in_sim=1 WHERE ID=?;", (item[2], ))
        conn.commit()
        cursor.execute("UPDATE id_factory SET RFID_ID=? WHERE ID=?;", (RFID_value,item[2], ))
        conn.commit()
        dist = FREE_CELL.pop(0)
        cursor.execute("UPDATE id_factory SET cell=? WHERE ID=?;", (dist,item[2], ))
        conn.commit()
        # поидее тут надо создавать объект карго и возвращать его?


        #######################################################
        ##              CREATE NEW CARGO                     ##

        new_cargo = cargo.Cargo(controller, RFID_value, destination=dist)
        storekepper.add_cargo(new_cargo)



        ######################################################
        WAIT_ITEM_RFID = False
        # rc_input.value = 'false'
        print(f'{item[2]} in sim, in_sim: {item[7]}')
        LAST_RFID = RFID_value

    conn.close()

#endregion



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

async def pallet3():
    await asyncio.gather(CT2.move_to('forward'), RC1_4.accept())
    await asyncio.gather(RC1_4.transit_next(), CT3.accept_to('forward'))
    await asyncio.gather(CT3.move_to('left'), CT3B.accept_to('right'))
    await asyncio.gather(CT3B.move_to('right'), RCb1.accept())

async def wtf():
    await asyncio.gather(pallet2(), pallet3())
### WOW 

async def database_routine():
    # проверяем расписание грузов
    print('database routine started')
    

    conn = sqlite3.connect('sim_data.sqlite')
    # cursor = conn.cursor()

    ## check pending DB entries
    item = find_pending_items(conn)
    if (item is not None):
        spawn__item(item)
        item = None

    
    #print('database routine ended')

async def produce_tasks():
    task_issued = True
    cargo_spawn = True
    while True:
        if cargo_spawn:
            new_cargo = cargo.Cargo(controller)
            await new_cargo.plan_route(1)
            pass
            
        await database_routine()

        if rs2_out.get_value() == False and task_issued:
            task_to_put = asyncio.create_task(controller.machines['RC1_4'].move())
            await controller.machines['RC1_4'].tasks.put(task_to_put)
            task_issued = False
        # if rs3_in.get_value() == False and not task_issued:
        #     task_to_put = asyncio.create_task(controller.machines['RC1_4'].transit_next())
        #     task_to_put2 = asyncio.create_task(controller.machines['CT3'].accept_to('forward'))

            # await controller.machines['RC1_4'].tasks.put(task_to_put)
        #     await controller.machines['CT3'].tasks.put(task_to_put2)
            # task_issued = False

        await asyncio.sleep(0.4)
        print('producer fired')

        
    


async def consume_tasks():
    while True:
        for mchne in controller.machines:
            await mchne.tasks.get()
        
        
        await asyncio.sleep(0.2)
        print('consumer fired')
            



async def za_loopu():
    
    start = time.perf_counter()

    
    produce = asyncio.create_task(produce_tasks())
    consume = asyncio.create_task(consume_tasks())

    #asyncio.gather(produce_tasks(), )
    await produce
    await consume




    
    elapsed = time.perf_counter() - start
    print('loop time: ' + elapsed)

    








if __name__ == '__main__':
    controller = fio.FIO_Controller(SIM_ADDRESS)

    storekepper = cargo.Storekeeper(controller)

    #region ####        DECLARATIONS      ####
    #region ###       TAG declaration      ###
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
    ## crossing conveyor entrance   CT 1
    ct1_plus =  controller.attach_tag("CT 1 (+)", tag_id='17862cd4-a781-4ee8-8f5b-12543abc0c12')
    ct1_min =   controller.attach_tag("CT 1 (-)", tag_id='54fd23dc-c971-4ce9-9561-46d223a0b786')
    ct1_left =  controller.attach_tag("CT 1 Left")
    ct1_right = controller.attach_tag("CT 1 Right")
    cs_1 =      controller.attach_tag("CS 1")
    stop_ct1 =  controller.attach_tag("StopR 1 Out")
    rs1_out  =  controller.attach_tag('RS 1 Out')
    ## crossing conveyor     CT 1A
    ct1a_plus =     controller.attach_tag("CT 1A (+)", tag_id='6ba24a7c-543c-4f84-bcb1-fc02ccc9078c')
    ct1a_min =      controller.attach_tag("CT 1A (-)", tag_id='f89666ca-4a6f-4af5-ac23-ba820d0b2597')
    ct1a_left =     controller.attach_tag("CT 1A Left") 
    ct1a_right =    controller.attach_tag("CT 1A Right")
    cs_1a =         controller.attach_tag("CS 1A")
    stop_ct1a =     controller.attach_tag("StopR 1A In")
    rs1a_out =      controller.attach_tag('RS 1A Out')
    ## crossing conveyor     CT 2
    ct2_plus =     controller.attach_tag("CT 2 (+)", tag_id='2ec8620c-d077-4fc7-bb67-14b08d4fd291')
    ct2_min =      controller.attach_tag("CT 2 (-)", tag_id='59455ffe-c196-423a-a1da-9606b261f0b2')
    ct2_left =     controller.attach_tag("CT 2 Left") 
    ct2_right =    controller.attach_tag("CT 2 Right")
    cs_2 =         controller.attach_tag("CS 2")
    #stop_ct1a =     controller.attach_tag("StopR 1A In")
    rs2_out =      controller.attach_tag('RS 2 Out')
    ## crossing conveyor   CT 3
    ct3_plus =  controller.attach_tag("CT 3 (+)", tag_id='15afa08d-9a9f-42e8-a8fe-1030d3224d56')
    ct3_min =   controller.attach_tag("CT 3 (-)", tag_id='8fe8c0f9-843f-4047-a56f-276b4767a4eb')
    ct3_left =  controller.attach_tag("CT 3 Left")
    ct3_right = controller.attach_tag("CT 3 Right")
    cs_3 =      controller.attach_tag("CS 3")
    stop_ct3 =  controller.attach_tag("StopR 3 Out")
    rs3_out  =  controller.attach_tag('RS 3 Out')
    ## crossing conveyor    CT 3B
    ct3b_plus =  controller.attach_tag("CT 3B (+)", tag_id='684f0b5d-4e28-4073-915d-ffa18005a595')
    ct3b_min =   controller.attach_tag("CT 3B (-)", tag_id='85e30eba-9486-4e32-80fc-31b9e643058b')
    ct3b_left =  controller.attach_tag("CT 3B Left")
    ct3b_right = controller.attach_tag("CT 3B Right")
    cs_3b =      controller.attach_tag("CS 3B")
    #stop_ct3b =  controller.attach_tag("StopR 3 Out")
    rs3b_out  =  controller.attach_tag('RS 3B Out to B')
    ## crossing conveyor    CT 4
    ct4_plus =  controller.attach_tag("CT 4 (+)", tag_id='77cfafe7-09ca-4f23-b97d-1f642de39478')
    ct4_min =   controller.attach_tag("CT 4 (-)", tag_id='f45c13d2-1aa3-44a1-b9ef-be456c407b4f')
    ct4_left =  controller.attach_tag("CT 4 Left")
    ct4_right = controller.attach_tag("CT 4 Right")
    cs_4 =      controller.attach_tag("CS 4")
    #stop_ct4 =  controller.attach_tag("StopR 4 Out")
    rs4_out  =  controller.attach_tag('RS 4 Out')
    ## crossing conveyor    CT 4B
    ct4b_plus =  controller.attach_tag("CT 4B (+)", tag_id='53688ecd-ab69-419f-8b7e-fcc3f47950dd')
    ct4b_min =   controller.attach_tag("CT 4B (-)", tag_id='937a6ec1-6bbd-4995-a6f5-41e14d6d0c6a')
    ct4b_left =  controller.attach_tag("CT 4B Left")
    ct4b_right = controller.attach_tag("CT 4B Right")
    cs_4b =      controller.attach_tag("CS 4B")
    #stop_ct4b =  controller.attach_tag("StopR 4B")
    rs4b_out  =  controller.attach_tag('RS 4B Out')
    ## conveyors CT1 -> CT2
    rc_1_2      = controller.attach_tag('RC (6m) 1.2')
    rc_1_3      = controller.attach_tag('RC (2m) 1.3')
    rs2_in      = controller.attach_tag('RS 2 In')
    ## conveyors CT2 -> CT3
    rc_1_4      = controller.attach_tag('RC (2m) 1.4')
    rs3_in      = controller.attach_tag('RS 3 In')
    ## conveyors CT3 -> CT4
    rc_1_5      = controller.attach_tag('RC (6m) 1.5')
    rc_1_6      = controller.attach_tag('RC (2m) 1.6')
    rs4_in      = controller.attach_tag('RS 4 In')
    #           RFID        #

    ## conveyors CT4B -> CT3B
    rcb8        = controller.attach_tag('RC B8')
    rcb9        = controller.attach_tag('RC B9')
    rs3b_in     = controller.attach_tag('RS 3B In')
    ## Conveyors curve 1A - Crane 1
    rc_a1 =     controller.attach_tag('RC A1')
    rcc_a2 =    controller.attach_tag('Curved RC A2')
    rc_a3 =     controller.attach_tag('RC A3')
    ## First crane arrivals
    l_rc_a4 =   controller.attach_tag('Load RC A4')
    al_a =      controller.attach_tag('At Load A')
    ## conveyor CT3B -> CTB
    rc_b1      = controller.attach_tag('RC B1')
    rsb_in     = controller.attach_tag('RS B In')

    ## cranes tags
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

    ##      CONVEYORS 
    RC1   = controller.attach_machine('RC1', fio.Conveyor(rc_input, rs1_in, (rfid_command, rfid_iec, rfid_iread, rfid_stat)))
    RCa1  = controller.attach_machine('RCa1', fio.Conveyor(rc_a1, al_a))
    RCCa2 = controller.attach_machine('RCCa2', fio.Conveyor(rcc_a2, al_a))  # arc start
    RCa3  = controller.attach_machine('RCa3', fio.Conveyor(rc_a3, al_a))
    lRCa4 = controller.attach_machine('lRCa4', fio.Conveyor(l_rc_a4, al_a) )# arc end
    RC1_4 = controller.attach_machine('RC1_4', fio.Conveyor(rc_1_4, rs3_in))
    RCb1  = controller.attach_machine('RCb1', fio.Conveyor(rc_b1, rsb_in))
    #endregion


    #region ##      CONVEYOR SERIES         ##
    Arc1    = controller.attach_machine('Arc1', fio.Conv_Series(al_a, rc_a1, rcc_a2, rc_a3, l_rc_a4))
    Bridge1 = controller.attach_machine('Bridge1', fio.Conv_Series(rs2_in, rc_1_2, rc_1_3)) # Between CT1 and CT2
    Bridge2 = controller.attach_machine('Bridge2', fio.Conv_Series(rs4_in, rc_1_5, rc_1_6)) # Between CT3 and CT4
    Bridge3 = controller.attach_machine('Bridge3', fio.Conv_Series(rs3b_in, rcb8, rcb9))    # Between CT3 and CT4
    #endregion

    #region ##      CROSSING CONVEYORS      ##
    CT1     = controller.attach_machine('CT1', fio.Crossing_conveyor(ct1_plus, ct1_min, ct1_left, ct1_right, cs_1, rs1_out, stop_ct1, wait_time=2.1))
    CT1A    = controller.attach_machine('CT1A', fio.Crossing_conveyor(ct1a_plus, ct1a_min, ct1a_left, ct1a_right, cs_1a, rs1a_out, stop_ct1a, wait_time=3.5))
    CT2     = controller.attach_machine('CT2', fio.Crossing_conveyor(ct2_plus, ct2_min, ct2_left, ct2_right, cs_2, rs2_out, wait_time=3.5))
    CT3     = controller.attach_machine('CT3', fio.Crossing_conveyor(ct3_plus, ct3_min, ct3_left, ct3_right, cs_3, rs3_out, wait_time=2.5))
    CT3B    = controller.attach_machine('CT3B', fio.Crossing_conveyor(ct3b_plus, ct3b_min, ct3b_left, ct3b_right, cs_3b, rs3b_out, wait_time=3.5))
    CT4     = controller.attach_machine('CT4', fio.Crossing_conveyor(ct4_plus, ct4_min, ct4_left, ct4_right, cs_4, rs4_out, wait_time=2.1))
    CT4B    = controller.attach_machine('CT4B', fio.Crossing_conveyor(ct4b_plus, ct4b_min, ct4b_left, ct4b_right, cs_4b, rs4b_out, wait_time=3.5))
    #endregion
    
        ##  CRANES
    Crane_A = controller.attach_machine('Crane_A', fio.Crane(mov_x_a, 
                                                            mov_z_a, 
                                                            targ_pos_a, 
                                                            at_mid_a, 
                                                            at_left_a, 
                                                            at_right_a, 
                                                            fork_left_a, 
                                                            fork_right_a, 
                                                            lift_a 
                                                            ))

    Crane_B = controller.attach_machine('Crane_B', fio.Crane(mov_x_b, 
                                                            mov_z_b, 
                                                            targ_pos_b, 
                                                            at_mid_b, 
                                                            at_left_b, 
                                                            at_right_b, 
                                                            fork_left_b, 
                                                            fork_right_b, 
                                                            lift_b 
                                                            ))


    #endregion      #####   END DECLARATION   #####


    # controller.sim_start()     doesnt work as expected
    controller.fetch_tags()


    #loop = asyncio.get_event_loop()  
    #asyncio.ensure_future(rc10.move())
    #asyncio.ensure_future(rc1.move())
    #  Перед запуском программы надо скзать базе данных что в симуляции ничего нет
    conn = sqlite3.connect('sim_data.sqlite')
    cursor = conn.cursor()
    cursor.execute("UPDATE id_factory SET in_sim=0")
    conn.commit()
    cursor.execute("UPDATE id_factory SET cell=0")
    conn.commit()
    cursor.execute("UPDATE id_factory SET RFID_ID=0")
    conn.commit()
    conn.close()

    asyncio.run(za_loopu())

    #while(True):
    '''loop = asyncio.get_event_loop()
    try:
        asyncio.ensure_future(task_control())
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        print("Closing Loop")
        loop.close()'''
    #asyncio.run( task_control() ) # _forever

    #asyncio.run(loop())
        #pass
        
    