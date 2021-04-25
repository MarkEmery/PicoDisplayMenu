# This example shows how to read the voltage from a lipo battery connected to a Raspberry Pi Pico via our Pico Lipo SHIM, and uses this reading to calculate how much charge is left in the battery.
# It then displays the info on the screen of Pico Display or Pico Explorer.
# Remember to save this code as main.py on your Pico if you want it to run automatically!

from machine import ADC, Pin
import utime
import picodisplay as display       # change "picodisplay" to "picoexplorer" if you're using a Pico Explorer

# # Set up and initialise display
# buf = bytearray(display.get_width() * display.get_height() * 2)
# display.init(buf)

vsys = ADC(29)              # reads the system input voltage
charging = Pin(24, Pin.IN)  # reading GP24 tells us whether or not USB power is connected
conversion_factor = 3 * 3.3 / 65535

full_battery = 4.2                  # these are our reference voltages for a full/empty battery, in volts
empty_battery = 2.8                 # the values could vary by battery size/manufacturer so you might need to adjust them

while True:
    voltage = vsys.read_u16() * conversion_factor
    percentage = 100 * ((voltage - empty_battery) / (full_battery - empty_battery))
    if percentage > 100:
        percentage = 100.00

    # draws the battery
    display.set_pen(0, 0, 0)
    display.clear()
    display.set_pen(190, 190, 190)
    display.rectangle(0, 0, 220, 135)
    display.rectangle(220, 40, 20, 55)
    display.set_pen(0, 0, 0)
    display.rectangle(3, 3, 214, 129)
    display.set_pen(0, 255, 0)
    display.rectangle(5, 5, round(210 / 100 * percentage), 125)

    # adding text
    display.set_pen(255, 0, 0)
    if charging.value() == 1:         # if it's plugged into USB power...
        display.text("Charging!", 15, 55, 240, 4)
    else:                             # if not, display the battery stats
        display.text('{:.2f}'.format(voltage) + "v", 15, 10, 240, 5)
        display.text('{:.0f}%'.format(percentage), 15, 50, 240, 5)

    display.update()
    utime.sleep(1)

    if display.is_pressed(display.BUTTON_X) and display.is_pressed(display.BUTTON_Y):
        display.set_pen(0, 0, 0)
        display.clear()
        display.set_pen(255, 0, 0)
        display.text("Rebooting..", 10, 10, 240, 2)
        display.update()
        time.sleep(0.1)
        machine.reset()

