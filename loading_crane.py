import requests
import json
from time import sleep
import time


import FactoryController as fio

SIM_ADDRESS = 'http://127.0.0.1:7410'    #my VM address
# GLOB_TIME = time.time()
# LIFT_TIME = 0

def item_to_shelf(number):
    # global LIFT_TIME
    fork_left_a.set_value(True)
    # fork_left_a.value = 'true'
    while(not(at_left_a.get_value())): sleep(0.05)
    # if (not(at_left_a.value)): 
    #     LIFT_TIME = time.time()
    #     return

    lift_a.set_value(True)
    # lift_a.value = 'true'
    # if (LIFT_TIME + 0.1 > time.time()):  return
    while(not(mov_z_a.get_value())): sleep(0.05)
    # if (mov_z_a.value): return
 
    fork_left_a.set_value(False)
    # fork_left_a.value = "false"
    while(not((at_mid_a.get_value()))): sleep(0.05)
    # if (not(at_mid_a.value)): return
    
    targ_pos_a.set_value(number)
    sleep(0.1)
    while (mov_z_a.get_value() or mov_x_a.get_value()): sleep(0.05)
    
    fork_left_a.set_value(True)
    while(not(at_left_a.get_value())): sleep(0.05)
   
    lift_a.set_value(False)
    sleep(0.1)
    while(mov_z_a.get_value()): sleep(0.05)
    
    fork_left_a.set_value(False)
    while(not(at_mid_a.get_value())): sleep(0.05)
    
    targ_pos_a.set_value(55)
    sleep(0.1)
    while(mov_z_a.get_value()) or mov_x_a.get_value(): sleep(0.05)


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
    
    while(True):
        controller.fetch_tags()
        item_to_shelf(15)
        controller.push_tags()