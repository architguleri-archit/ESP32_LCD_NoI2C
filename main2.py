from machine import Pin
from time import sleep, ticks_ms

# --- LCD pin connections ---
# RS, E, D4, D5, D6, D7
rs = Pin(21, Pin.OUT)
en = Pin(22, Pin.OUT)
d4 = Pin(18, Pin.OUT)
d5 = Pin(19, Pin.OUT)
d6 = Pin(23, Pin.OUT)
d7 = Pin(5, Pin.OUT)

led = Pin(2, Pin.OUT)  # On-board LED

lcdWidth = 16
lcdHeight = 2

line1 = "THANKS"
line2 = "FOR WATCHING"

# Helper functions for LCD control
def pulse_enable():
    en.off()
    sleep(0.0005)
    en.on()
    sleep(0.0005)
    en.off()
    sleep(0.0005)

def send_nibble(data):
    d4.value((data >> 0) & 1)
    d5.value((data >> 1) & 1)
    d6.value((data >> 2) & 1)
    d7.value((data >> 3) & 1)
    pulse_enable()

def send_byte(data, rs_val):
    rs.value(rs_val)
    send_nibble(data >> 4)
    send_nibble(data & 0x0F)
    sleep(0.001)

def lcd_cmd(cmd):
    send_byte(cmd, 0)

def lcd_data(data):
    send_byte(data, 1)

def lcd_clear():
    lcd_cmd(0x01)
    sleep(0.002)

def lcd_set_cursor(col, row):
    row_offsets = [0x00, 0x40]
    lcd_cmd(0x80 | (col + row_offsets[row]))

def lcd_print(text):
    for ch in text:
        lcd_data(ord(ch))

def lcd_create_char(location, charmap):
    location &= 0x7
    lcd_cmd(0x40 | (location << 3))
    for line in charmap:
        lcd_data(line)

def lcd_init():
    sleep(0.02)
    send_nibble(0x03)
    sleep(0.005)
    send_nibble(0x03)
    sleep(0.0002)
    send_nibble(0x03)
    send_nibble(0x02)  # 4-bit mode
    lcd_cmd(0x28)  # 2 lines, 5x8 font
    lcd_cmd(0x0C)  # Display on, cursor off
    lcd_cmd(0x06)  # Entry mode
    lcd_clear()

# Define smiley face
def define_custom_chars():
    smiley = [
        0b00000,
        0b01010,
        0b01010,
        0b00000,
        0b00000,
        0b10001,
        0b01110,
        0b00000
    ]
    lcd_create_char(6, smiley)

def clear_line(line):
    lcd_set_cursor(0, line)
    lcd_print(" " * lcdWidth)
    lcd_set_cursor(0, line)

# Map function equivalent to Arduino's map()
def map_value(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

# Boot animation
def boot_animation():
    total_steps = 100
    lcd_delay = 0.08
    led_state = 0
    last_blink = ticks_ms()

    clear_line(0)
    clear_line(1)

    for percent in range(total_steps + 1):
        chars_to_fill = (percent * lcdWidth) // 100

        # Progress bar
        lcd_set_cursor(0, 0)
        for i in range(lcdWidth):
            lcd_data(255 if i < chars_to_fill else ord(' '))

        # Loading text
        lcd_set_cursor(0, 1)
        lcd_print("Loading: ")
        if percent < 10:
            lcd_print(" ")
        lcd_print(str(percent) + "%   ")

        # LED blink faster as % increases
        blink_interval = map_value(percent, 0, total_steps, 400, 50)
        if ticks_ms() - last_blink >= blink_interval:
            led_state = not led_state
            led.value(led_state)
            last_blink = ticks_ms()

        sleep(lcd_delay)

    led.off()
    clear_line(0)
    clear_line(1)

# Typewriter "PLEASE SUBSCRIBE :)"
def typewriter_reveal_animation(duration_seconds=10):
    reveal_text = "PLEASE SUBSCRIBE "
    typing_delay = 0.15

    clear_line(0)
    clear_line(1)
    lcd_set_cursor(0, 1)

    for i, ch in enumerate(reveal_text):
        lcd_print(ch)
        sleep(typing_delay)

    lcd_data(6)  # smiley

    start_time = ticks_ms()
    while ticks_ms() - start_time < duration_seconds * 1000:
        led.on()
        sleep(0.5)
        led.off()
        sleep(0.5)

    led.off()
    clear_line(0)
    clear_line(1)

# --- Main ---
lcd_init()
define_custom_chars()
lcd_clear()

def main():
    boot_animation()
    lcd_clear()

    start_col1 = (lcdWidth - len(line1)) // 2
    start_col2 = (lcdWidth - (len(line2) + 2)) // 2

    for _ in range(4):
        clear_line(1)
        lcd_set_cursor(start_col1, 0)
        lcd_print(line1)
        led.on()
        sleep(0.4)

        clear_line(0)
        lcd_set_cursor(start_col2, 1)
        lcd_print(line2)
        lcd_print(" ")
        lcd_data(6)
        led.off()
        sleep(0.4)

    # Final state
    clear_line(0)
    lcd_set_cursor(start_col1, 0)
    lcd_print(line1)

    clear_line(1)
    lcd_set_cursor(start_col2, 1)
    lcd_print(line2)
    lcd_print(" ")
    lcd_data(6)

    typewriter_reveal_animation(10)

# Run main loop forever
while True:
    main()
