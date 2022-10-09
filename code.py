# Originally coded by Novaspirit Tech
# Copy this code into your code.py file.
import time
import usb_hid
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
import board
import digitalio
import mfrc522
import busio

# These are the corresponding GPIOs on the Pi Pico
# that you soldered

btn1_pin = board.GP16
btn2_pin = board.GP15
btn3_pin = board.GP14
btn4_pin = board.GP8
btn5_pin = board.GP7
btn6_pin = board.GP6
btn7_pin = board.GP12
btn8_pin = board.GP11
btn9_pin = board.GP10

btn1 = digitalio.DigitalInOut(btn1_pin)
btn1.direction = digitalio.Direction.INPUT
btn1.pull = digitalio.Pull.DOWN

btn2 = digitalio.DigitalInOut(btn2_pin)
btn2.direction = digitalio.Direction.INPUT
btn2.pull = digitalio.Pull.DOWN

btn3 = digitalio.DigitalInOut(btn3_pin)
btn3.direction = digitalio.Direction.INPUT
btn3.pull = digitalio.Pull.DOWN

btn4 = digitalio.DigitalInOut(btn4_pin)
btn4.direction = digitalio.Direction.INPUT
btn4.pull = digitalio.Pull.DOWN

btn5 = digitalio.DigitalInOut(btn5_pin)
btn5.direction = digitalio.Direction.INPUT
btn5.pull = digitalio.Pull.DOWN

btn6 = digitalio.DigitalInOut(btn6_pin)
btn6.direction = digitalio.Direction.INPUT
btn6.pull = digitalio.Pull.DOWN

btn7 = digitalio.DigitalInOut(btn7_pin)
btn7.direction = digitalio.Direction.INPUT
btn7.pull = digitalio.Pull.DOWN

btn8 = digitalio.DigitalInOut(btn8_pin)
btn8.direction = digitalio.Direction.INPUT
btn8.pull = digitalio.Pull.DOWN

btn9 = digitalio.DigitalInOut(btn9_pin)
btn9.direction = digitalio.Direction.INPUT
btn9.pull = digitalio.Pull.DOWN

keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

led_red = digitalio.DigitalInOut(board.GP18)
led_red.direction = digitalio.Direction.OUTPUT

led_blue = digitalio.DigitalInOut(board.GP19)
led_blue.direction = digitalio.Direction.OUTPUT

# RFID Reader Setting
sck = board.GP2
mosi = board.GP3
miso = board.GP4
spi = busio.SPI(sck, MOSI=mosi, MISO=miso)

cs = digitalio.DigitalInOut(board.GP1)
rst = digitalio.DigitalInOut(board.GP0)
rfid = mfrc522.MFRC522(spi, cs, rst)
rfid.set_antenna_gain(0x07 << 4)

password1 = "password1\n"
password2 = "password2(\n"
password_git = "password3\n"
password_one_pass = "password4\n"

licensed_rfids = ['73065136', '07d16a92', 'd12e7365', 'c332ddc7'] 

def blink_red(s=0.1, t=1):
    for x in range(t):
        led_red.value = True
        time.sleep(s)
        led_red.value = False
        time.sleep(s)


def blink_blue(s=0.1, t=1):
    for x in range(t):
        led_blue.value = True
        time.sleep(s)
        led_blue.value = False
        time.sleep(s)
    
    
def get_press_one():
    key = -1
    if btn1.value:
        key = 1
    elif btn2.value:
        key = 2
    elif btn3.value:
        key = 3
    elif btn4.value:
        key = 4
    elif btn5.value:
        key = 5
    elif btn6.value:
        key = 6
    elif btn7.value:
        key = 7
    elif btn8.value:
        key = 8
    elif btn9.value:
        key = 9
        
    #time.sleep(0.1)
    return key


def is_valid_password(password):
    print(password)
    #time.sleep(0.5)
    blink_blue(t=1)
    i = 0
    while True:
        key = get_press_one()
            
        if key < 0:
            continue
        
        p = password[i]
        print(f"key: {key} p: {p} i: {i}")
        if str(key) != p:
            blink_red(t=3)
            return False
        else:
            blink_blue()
            print(p)
        
        i = i + 1
        if len(password) <= i:
            break
        #time.sleep(0.05)
    return True


def licensed_rfid():    
    (status, tag_type) = rfid.request(rfid.REQALL)
    if status == rfid.OK:
        (status, raw_uid) = rfid.anticoll()

        if status == rfid.OK:
            rfid_data = "{:02x}{:02x}{:02x}{:02x}".format(raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
    else:
        rfid_data = ""
    #if rfid_data != "":
    #    print(rfid_data)
    return rfid_data in licensed_rfids


def check_rfid(timeout=3):
    is_licensed = False
    try:
        led_blue.value = True
        prev_time = time.monotonic()
        while True:
            if licensed_rfid():
                is_licensed = True
                break
            now_time = time.monotonic()
            if now_time - prev_time > timeout:
                break
            time.sleep(0.1)
    finally:
        led_blue.value = False
    return is_licensed


while True:
    if btn1.value: #1
        if btn9.value:
            if check_rfid():
               layout.write(password1)
               time.sleep(0.1)
        else:
            keyboard.send(Keycode.F1)
            time.sleep(0.1)
    if btn2.value: #2
        if btn9.value:
            if check_rfid():
               layout.write(password2)
               time.sleep(0.1)
        else:
            keyboard.send(Keycode.F2)
            time.sleep(0.1)
    if btn3.value: #3
        if btn9.value:
            if check_rfid():
               layout.write(password_git)
               time.sleep(0.1)
        else:
            keyboard.send(Keycode.F3)
            time.sleep(0.1)
    if btn4.value: #4
        if btn9.value:
            if check_rfid():
               layout.write(password_one_pass)
               time.sleep(0.1)
        else:
            keyboard.send(Keycode.F4)
            time.sleep(0.1)
    if btn5.value: #5
        keyboard.send(Keycode.F5)
        time.sleep(0.1)
    if btn6.value: #6
        keyboard.send(Keycode.F6)
        time.sleep(0.1)
    if btn7.value: #7
        keyboard.send(Keycode.F7)
        time.sleep(0.1)
    if btn8.value: #8
        keyboard.send(Keycode.F8)
        time.sleep(0.1)
    if btn9.value: #9
        pass
