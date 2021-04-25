
def do_update():
    display.set_backlight(brightness)
    display.set_pen(0, 0, 0)
    display.clear()
    display.set_pen(255, 0, 0)
    display.text(str(brightness), 10, 10, 240, 2)
    display.update()

while True:
    if display.is_pressed(display.BUTTON_A):
        brightness = brightness + 0.1
        if brightness > 1:
            brightness = 1
        do_update()
    elif display.is_pressed(display.BUTTON_B):
        brightness = brightness - 0.1
        if brightness < 0.2:
            brightness = 0.2
        do_update()
    elif display.is_pressed(display.BUTTON_X) and display.is_pressed(display.BUTTON_Y):
        f = open("/brightness.val", "w")
        f.write(str(brightness))
        f.close()
        display.set_pen(0, 0, 0)
        display.clear()
        display.set_pen(255, 0, 0)
        display.text("Rebooting..", 10, 10, 240, 2)
        display.update()
        time.sleep(0.1)
        machine.reset()

    utime.sleep(0.1)
