from micropython import const
from machine import Pin, SPI, Timer
from random import choice
import framebuf

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

spi = SPI(0)
display = Matrix8x8(spi, Pin(5), 4)

running_matrix = [
    [1] * 8 + [0] * 24 for i in range(8)
    ]

def change_display(matrix):
    for i in range(32):
        for j in range(8):
            display.pixel(i, j, matrix[j][i])
    display.show()

def get_valid_rows(matrix):
    return [i for i in range(8) if matrix[i] != 24 * [0] + 8 * [1]]
    
def progress_row(matrix, row_no):
    valid_indices = [
        i for i in range(31) if (matrix[row_no][i] == 1) and (matrix[row_no][i+1] == 0)
        ]
    chosen_index = choice(valid_indices)
    matrix[row_no][chosen_index + 1] = 1
    matrix[row_no][chosen_index] = 0
    return matrix

def progress_one_step():
    global running_matrix
    running_matrix = progress_row(running_matrix, choice(get_valid_rows(running_matrix)))
    change_display(running_matrix)

tim = Timer(period=1000, mode=Timer.PERIODIC, callback=lambda x:progress_one_step())
        
