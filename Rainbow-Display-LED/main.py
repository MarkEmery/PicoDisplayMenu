## This example borrows a CircuitPython hsv_to_rgb function to cycle through some rainbows on Pico Display's screen and RGB LED . If you're into rainbows, HSV (Hue, Saturation, Value) is very useful!

# From CPython Lib/colorsys.py
def hsv_to_rgb(h, s, v):
    if s == 0.0:
        return v, v, v
    i = int(h*6.0)
    f = (h*6.0) - i
    p = v*(1.0 - s)
    q = v*(1.0 - s*f)
    t = v*(1.0 - s*(1.0-f))
    i = i%6
    if i == 0:
        return v, t, p
    if i == 1:
        return q, v, p
    if i == 2:
        return p, v, t
    if i == 3:
        return p, q, v
    if i == 4:
        return t, p, v
    if i == 5:
        return v, p, q

h = 0

while True:
    h += 1
    r, g, b = [int(255 * c) for c in hsv_to_rgb(h / 360.0, 1.0, 1.0)]  # rainbow magic
    display.set_led(r, g, b)  # Set LED to a converted HSV value
    display.set_pen(r, g, b)  # Set pen to a converted HSV value
    display.clear()           # Fill the screen with the colour
    display.set_pen(0, 0, 0)  # Set pen to black
    display.text("Pimo Roni :^)", 10, 10, 240, 6)  # Add some text
    display.update()          # Update the display
    utime.sleep(1.0 / 60)  
    if display.is_pressed(display.BUTTON_X) and display.is_pressed(display.BUTTON_Y):
        display.set_pen(0, 0, 0)
        display.clear()
        display.set_pen(255, 0, 0)
        display.text("Rebooting..", 10, 10, 240, 2)
        display.update()
        time.sleep(0.1)
        machine.reset()
