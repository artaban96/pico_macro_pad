import storage
import board
import digitalio

btn9_pin = board.GP10

btn9 = digitalio.DigitalInOut(btn9_pin)
btn9.direction = digitalio.Direction.INPUT
btn9.pull = digitalio.Pull.DOWN

if not btn9.value:
    print(f"boot: button not pressed, disabling drive")
    storage.disable_usb_drive()
else:
    print(f"boot: button pressed, enabling drive")
