from led_bar import set_all, set_pixel, show
from buzzer import affirmative, wrong_input
from time import sleep
from _thread import start_new_thread

flash_frequency = 10
flash_count = 10


def handle_user_input(inputstring, valid_strings_list):
    if any([x.startswith(inputstring) for x in valid_strings_list]):
        if inputstring.endswith('#'):
            success()
            return inputstring, True
        else:
            show_result(len(inputstring) - 1)
            return inputstring, False
    else:
        if inputstring.endswith('*'):
            show_result(0)
            return '*', False
        else:
            flash_red()
            return '', False

def flash_red():
    start_new_thread(wrong_input, ())
    for _ in range(flash_count):
        set_all(255, 0, 0)
        show()
        sleep(1 / flash_frequency)
        set_all(0, 0, 0)
        show()
        sleep(1 / flash_frequency)


def show_result(length):
    start_new_thread(affirmative, ())
    for i in range(length):
        set_pixel(2*i, 0, 160, 50)
        set_pixel(2*i + 1, 0, 160, 50)
    for i in range(length, 4):
        set_pixel(2*i, 40, 30, 0)
        set_pixel(2*i + 1, 40, 30, 0)
    show()


def success():
    start_new_thread(affirmative, ())
    for _ in range(flash_count):
        set_all(0, 255, 0)
        show()
        sleep(1 / flash_frequency)
        set_all(0, 0, 0)
        show()
        sleep(1 / flash_frequency)
