from machine import Pin, Timer, RTC
from random import random
from time import sleep


rtc = RTC()
rtc.datetime((1,1,1,0,0,0,0,0))


def cycle(list):
     current = 0
     while True:
         if current < len(list):
             yield list[current]
             current += 1
         else:
             yield list[0]
             current = 1


class led_traffic_lights:
    def __init__(self, red, yellow, green):
        self.red_led = Pin(red, Pin.OUT, value=1)
        self.yellow_led = Pin(yellow, Pin.OUT, value=0)
        self.green_led = Pin(green, Pin.OUT, value=0)
    
    def set_status(self, red, yellow, green):
        self.red_led.value(red)
        self.yellow_led.value(yellow)
        self.green_led.value(green)


class crossing():
    def __init__(self, dir_1_list, dir_2_list):
        self.dir_1_list = dir_1_list
        self.dir_2_list = dir_2_list
        self.set_status_1(1,0,0)
        self.set_status_2(0,0,1)
    
    def set_status_1(self, red, yellow, green):
        for lights in self.dir_1_list:
            lights.set_status(red, yellow, green)
    
    def set_status_2(self, red, yellow, green):
        for lights in self.dir_2_list:
            lights.set_status(red, yellow, green)


class crossing_timings():
    def __init__(self, cross, yellow_phase, both_red_phase, dir_1_green_phase, dir_2_green_phase, indicator_led, indicator_blink_speed):
        self.cross = cross
        self.indicator_led = indicator_led
        self.ibs = indicator_blink_speed
        self.state_cycle = cycle(
                [
                    ('d2g', (1,0,0), (0,0,1), dir_1_green_phase),
                    ('y1ad2g', (1,0,0), (0,1,0), yellow_phase),
                    ('rad2g', (1,0,0), (1,0,0), both_red_phase),
                    ('y2ad2g', (1,1,0), (1,0,0), yellow_phase),
                    ('d1g', (0,0,1), (1,0,0), dir_2_green_phase),
                    ('y1ad1g', (0,1,0), (1,0,0), yellow_phase),
                    ('rad1g', (1,0,0), (1,0,0), both_red_phase),
                    ('y2ad1g', (1,0,0), (1,1,0), yellow_phase)
                ]
            )
        self.main_timer = Timer()
        self.blink_timer = Timer()
    
    def toggle_led(self, timer):
        self.indicator_led.toggle()
    
    def switch_state(self, timer):
        self.blink_timer.deinit()
        self.state = next(self.state_cycle)
        self.last_state_change = rtc.datetime()
        self.main_timer.init(
            period=self.state[3] * 1000,
            mode=Timer.ONE_SHOT,
            callback=self.switch_state
            )
        self.cross.set_status_1(*self.state[1])
        self.cross.set_status_2(*self.state[2])
        self.indicator_led.off()
    
    def run(self):
        self.switch_state(self.main_timer)


def speed_up_change(cross_timing):
    if cross_timing.state[0] in ['d1g', 'd2g']:
        timediff = [t[0]-t[1] for t in zip(rtc.datetime(), cross_timing.last_state_change)]
        time_since_trigger = timediff[-4] * 3600 + timediff[-3] * 60 + timediff[-2]
        if cross_timing.state[3] - time_since_trigger > 3:
            cross_timing.main_timer.init(
                period=3000,
                mode=Timer.ONE_SHOT,
                callback=cross_timing.switch_state
                )
        cross_timing.blink_timer.init(
            period=int(cross_timing.ibs * 1000.0),
            mode=Timer.PERIODIC,
            callback=cross_timing.toggle_led
            )


button_pin = Pin(17, Pin.IN, Pin.PULL_UP)


onboard_led = Pin(25, Pin.OUT, 0)


tl1 = led_traffic_lights(2, 3, 4)
tl2 = led_traffic_lights(13, 12, 11)


crossing1 = crossing(
    [tl1], [tl2]
    )
cross_timing1 = crossing_timings(
    crossing1,
    2,
    1,
    30,
    40,
    onboard_led,
    0.1
    )
button_pin.irq(
    handler = lambda p: speed_up_change(cross_timing1),
    trigger = Pin.IRQ_FALLING
    )


cross_timing1.run()

