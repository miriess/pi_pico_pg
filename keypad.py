from machine import Pin
from time import sleep
from sys import exit
from picoblinkt import set_brightness, set_pixel, show, set_all

column_list = [20, 19, 18]
row_list = [10, 11, 12, 13]

keypad_matrix = [
    ['1', '4', '7', '*'],
    ['2', '5', '8', '0'],
    ['3', '6', '9', '#']
]

set_brightness(0.04)


def initialize_pins():
    column_pins = [
        Pin(i, Pin.IN, Pin.PULL_UP) for i in column_list
    ]
    row_pins = [
        Pin(j, Pin.OUT, 0) for j in row_list
    ]
    return column_pins, row_pins


def reverse_readout_pins(col_id):
    column_pins = [
        Pin(i, Pin.OUT, 0) for i in column_list
    ]
    row_pins = [
        Pin(j, Pin.IN, Pin.PULL_UP) for j in row_list
    ]
    for j, gpiopin in enumerate(row_pins):
        if gpiopin.value() == 0:
            handle_result(col_id, j)
            break


def get_value_for_column(col_id):
    reverse_readout_pins(col_id)
    sleep(1)
    return initialize_pins()



def handle_result(i, j):
    result = keypad_matrix[i][j]
    print(result)
    if result in ['*', '#']:
        set_all(255, 255, 0)
    elif int(result) % 2 == 0:
        set_all(255, 0, 0)
    else:
        set_all(0, 255, 255)
    show()


CP, RP = initialize_pins()

while True:
    for i, gpiopin in enumerate(CP):
        if gpiopin.value() == 0:
            CP, RP = get_value_for_column(i)
            break
