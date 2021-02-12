import requests
import json
from time import sleep
import time, datetime
import asyncio
import sqlite3

import FactoryController as fio

SIM_ADDRESS = 'http://127.0.0.1:7410'    #my VM address


async def task_controll():
    await asyncio.gather(Crane_A.to_shelf(15), Crane_B.to_shelf(20))
    
    await asyncio.gather(Crane_A.to_shelf(15), Crane_B.from_shelf(20))
    # while(True):
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

    # debag - resert db 
    conn = sqlite3.connect('sim_data.sqlite')
    cursor = conn.cursor()
    cursor.execute("UPDATE id_factory SET in_sim=0")
    conn.commit()
    conn.close()
    
       
    asyncio.run( task_controll() )

