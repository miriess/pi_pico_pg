from micropython import const
from machine import Pin, SPI, Timer
from random import choice
from time import sleep
import framebuf
from math import floor

_NOOP = const(0)
_DIGIT0 = const(1)
_DECODEMODE = const(9)
_INTENSITY = const(10)
_SCANLIMIT = const(11)
_SHUTDOWN = const(12)
_DISPLAYTEST = const(15)

class Matrix8x8:
    def __init__(self, spi, cs, num):
        """
        Driver for cascading MAX7219 8x8 LED matrices.
        >>> import max7219
        >>> from machine import Pin, SPI
        >>> spi = SPI(1)
        >>> display = max7219.Matrix8x8(spi, Pin('X5'), 4)
        >>> display.text('1234',0,0,1)
        >>> display.show()
        """
        self.spi = spi
        self.cs = cs
        self.cs.init(cs.OUT, True)
        self.buffer = bytearray(8 * num)
        self.num = num
        fb = framebuf.FrameBuffer(self.buffer, 8 * num, 8, framebuf.MONO_HLSB)
        self.framebuf = fb
        # Provide methods for accessing FrameBuffer graphics primitives. This is a workround
        # because inheritance from a native class is currently unsupported.
        # http://docs.micropython.org/en/latest/pyboard/library/framebuf.html
        self.fill = fb.fill  # (col)
        self.pixel = fb.pixel # (x, y[, c])
        self.hline = fb.hline  # (x, y, w, col)
        self.vline = fb.vline  # (x, y, h, col)
        self.line = fb.line  # (x1, y1, x2, y2, col)
        self.rect = fb.rect  # (x, y, w, h, col)
        self.fill_rect = fb.fill_rect  # (x, y, w, h, col)
        self.text = fb.text  # (string, x, y, col=1)
        self.scroll = fb.scroll  # (dx, dy)
        self.blit = fb.blit  # (fbuf, x, y[, key])
        self.init()

    def _write(self, command, data):
        self.cs(0)
        for m in range(self.num):
            self.spi.write(bytearray([command, data]))
        self.cs(1)

    def init(self):
        for command, data in (
            (_SHUTDOWN, 0),
            (_DISPLAYTEST, 0),
            (_SCANLIMIT, 7),
            (_DECODEMODE, 0),
            (_SHUTDOWN, 1),
        ):
            self._write(command, data)

    def brightness(self, value):
        if not 0 <= value <= 15:
            raise ValueError("Brightness out of range")
        self._write(_INTENSITY, value)

    def show(self):
        for y in range(8):
            self.cs(0)
            for m in range(self.num):
                self.spi.write(bytearray([_DIGIT0 + y, self.buffer[(y * self.num) + m]]))
            self.cs(1)

        
class sandClock:
    def __init__(self, total_time, num_rows, brightness, spi, cs_pin, matrix_count=4, no_blinks=20):
        self.num_rows = num_rows
        self.total_rows = matrix_count * 8
        self.total_time = total_time
        self.target_col =  [0] * (self.total_rows - num_rows) + [1] * num_rows
        self.matrix = [
            [1] * num_rows + [0] * (self.total_rows - num_rows) for i in range(8)
            ]
        self.tick_length = floor(
            total_time * 1000 / (8 * num_rows * (self.total_rows - num_rows))
            )
        self.display = Matrix8x8(spi, cs_pin, matrix_count)
        self.display.brightness(brightness)
        self.display.text('10"', 0, 0)
        self.display.show()
        sleep(10)
        self.change_display()
        self.no_blinks = no_blinks
        self.blinks_to_go = no_blinks
        self.next_blink_state = 1
        self.calculate_valid_cols()
        print(self.valid_cols)
        self.blink_timer = Timer()
        self.main_timer = Timer(
            period=self.tick_length,
            mode=Timer.PERIODIC,
            callback=self.one_step
            )
    
    def change_display(self):
        for i in range(self.total_rows):
            for j in range(8):
                self.display.pixel(i, j, self.matrix[j][i])
        self.display.show()
    
    def calculate_valid_cols(self):
        self.valid_cols = [
            i for i in range(8) if self.matrix[i] != self.target_col
            ]
    
    def progress_col(self, col_id):
        valid_indices = [
            i for i in range(self.total_rows - 1)
            if (self.matrix[col_id][i] == 1) and (self.matrix[col_id][i+1] == 0)
            ]
        chosen_index = choice(valid_indices)
        self.matrix[col_id][chosen_index + 1] = 1
        self.matrix[col_id][chosen_index] = 0
    
    def one_step(self, timer):
        self.progress_col(
            choice(self.valid_cols)
            )
        self.change_display()
        self.calculate_valid_cols()
        if len(self.valid_cols) == 0:
            self.main_timer.deinit()
            sleep(0.5)
            self.blink_timer.init(
                period=500,
                mode=Timer.PERIODIC,
                callback=self.blink
            )
    
    def blink(self, timer):
        self.display.fill(self.next_blink_state)
        self.display.show()
        self.next_blink_state = 0 if self.next_blink_state else 1
        self.blinks_to_go -= 1
        if self.blinks_to_go == 0:
            self.blink_timer.deinit()
            self.matrix = [
                [1] * self.num_rows + [0] * (self.total_rows - self.num_rows) for i in range(8)
                ]
            self.calculate_valid_cols()
            self.change_display()
            self.display.show()
            self.next_blink_state = 1
            self.blinks_to_go = self.no_blinks
            self.main_timer.init(
                period=self.tick_length,
                mode=Timer.PERIODIC,
                callback=self.one_step
                )

spi = SPI(0)
cs_pin = Pin(5)

sc = sandClock(300, 12, 1, spi, cs_pin)
