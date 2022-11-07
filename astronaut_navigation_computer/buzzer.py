from machine import Pin
from time import sleep

onpin = Pin(5, Pin.OUT, value=0)

def affirmative():
    onpin.value(1)
    sleep(0.05)
    onpin.value(0)
    sleep(0.1)
    onpin.value(1)
    sleep(0.1)
    onpin.value(0)

def wrong_input():
    onpin.value(1)
    sleep(0.08)
    onpin.value(0)
    sleep(0.05)
    onpin.value(1)
    sleep(0.08)
    onpin.value(0)
    sleep(0.05)
    onpin.value(1)
    sleep(0.08)
    onpin.value(0)
