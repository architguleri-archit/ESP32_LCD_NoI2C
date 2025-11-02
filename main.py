from machine import Pin
from time import sleep_ms

# Simple LiquidCrystal class for 4-bit LCD (no I2C)
class LiquidCrystal:
    def __init__(self, rs, en, d4, d5, d6, d7):
        self.rs = Pin(rs, Pin.OUT)
        self.en = Pin(en, Pin.OUT)
        self.data_pins = [Pin(d4, Pin.OUT), Pin(d5, Pin.OUT), Pin(d6, Pin.OUT), Pin(d7, Pin.OUT)]
        self.lcd_init()

    def pulse_enable(self):
        self.en.off()
        sleep_ms(1)
        self.en.on()
        sleep_ms(1)
        self.en.off()
        sleep_ms(1)

    def send_nibble(self, data):
        for i in range(4):
            self.data_pins[i].value((data >> i) & 1)
        self.pulse_enable()

    def send_byte(self, data, char_mode=False):
        self.rs.value(char_mode)
        self.send_nibble(data >> 4)
        self.send_nibble(data & 0x0F)
        sleep_ms(2)

    def command(self, cmd):
        self.send_byte(cmd, False)

    def write(self, char):
        self.send_byte(ord(char), True)

    def print(self, text):
        for char in text:
            self.write(char)

    def setCursor(self, col, row):
        row_offsets = [0x00, 0x40]
        self.command(0x80 | (col + row_offsets[row]))

    def begin(self, cols, rows):
        self.cols = cols
        self.rows = rows
        # Standard LCD initialization
        sleep_ms(50)
        self.send_nibble(0x03)
        sleep_ms(5)
        self.send_nibble(0x03)
        sleep_ms(1)
        self.send_nibble(0x03)
        self.send_nibble(0x02)
        self.command(0x28)
        self.command(0x0C)
        self.command(0x06)
        self.command(0x01)
        sleep_ms(2)

    def lcd_init(self):
        self.begin(16, 2)

# Pin mapping: RS, E, D4, D5, D6, D7
lcd = LiquidCrystal(21, 22, 18, 19, 23, 5)

# Setup section
lcd.print("Hello, ESP32!")
lcd.setCursor(0, 1)
lcd.print("No I2C Module")

# Loop section (empty)
while True:
    pass
