from machine import Pin
from neopixel import NeoPixel
from time import sleep

sleeptime = 0.5

np_pow = Pin(11, Pin.OUT, value=1)
np_dat = Pin(12, Pin.OUT)
np_arr = NeoPixel(np_dat, 1)

green_pix = Pin(16, Pin.OUT, value=1)   # 1 is off for these
red_pix = Pin(17, Pin.OUT, value=1)
blue_pix = Pin(25, Pin.OUT, value=1)

def set_pixels(red: int, green: int, blue: int) -> None:
    green_pix.value((green + 1) % 2)
    red_pix.value((red + 1) % 2)
    blue_pix.value((blue + 1) % 2)

combinations = [
    [1,1,1],
    [1,1,0],
    [1,0,1],
    [0,1,1],
    [1,0,0],
    [0,1,0],
    [0,0,1],
    [0,0,0]
]

np_pow.value(1)

while True:
    for comb in combinations:
        set_pixels(*comb)
        np_arr[0] = [50*colval for colval in comb]
        np_arr.write()
        sleep(sleeptime)
