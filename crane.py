import requests
import json
from time import sleep
import time
import asyncio

import FactoryController as fio

SIM_ADDRESS = 'http://127.0.0.1:7410'    #my VM address


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
    # Сначала выполняется это до конца
    await asyncio.gather(item_to_shelf_A(15), item_to_shelf_B(29))
    # потом выполняется это
    await asyncio.gather(item_from_shelf_A(15), item_from_shelf_B(29))





if __name__ == '__main__':
    controller = fio.FIO_Controller(SIM_ADDRESS)
    ##  Tag declaration
    print('Tag declaration')
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


    
       
    asyncio.run( task_controll() )

