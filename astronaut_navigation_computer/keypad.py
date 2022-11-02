from machine import Pin

column_list = [20, 19, 18]
row_list = [10, 11, 12, 13]

keypad_matrix = [
    ['1', '4', '7', '*'],
    ['2', '5', '8', '0'],
    ['3', '6', '9', '#']
]


def initialize_pins():
    column_pins = [
        Pin(i, Pin.IN, Pin.PULL_UP) for i in column_list
    ]
    row_pins = [
        Pin(j, Pin.OUT, 0) for j in row_list
    ]
    return column_pins, row_pins


def get_value_for_column(col_id):
    column_pins = [
        Pin(i, Pin.OUT, 0) for i in column_list
    ]
    row_pins = [
        Pin(j, Pin.IN, Pin.PULL_UP) for j in row_list
    ]
    for j, gpiopin in enumerate(row_pins):
        if gpiopin.value() == 0:
            initialize_pins()
            return keypad_matrix[col_id][j]
    initialize_pins()
    return ''


def get_user_input():
    CP, RP = initialize_pins()
    while True:
        for i, gpiopin in enumerate(CP):
            if gpiopin.value() == 0:
                return get_value_for_column(i)


if __name__ == '__main__':
    CP, RP = initialize_pins()

    while True:
        for i, gpiopin in enumerate(CP):
            if gpiopin.value() == 0:
                CP, RP = get_value_for_column(i)
                break
