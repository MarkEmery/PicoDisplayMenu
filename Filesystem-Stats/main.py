import time
import os

path = "/"
info = os.statvfs(path)
print(info)
f_bsize = "File system block size:" + str(info[0])
f_bfree = "# of free blocks:" + str(info[3])
display.set_pen(0, 0, 0)
display.clear()
display.set_pen(255, 255, 255)
display.text(f_bsize, 10, 10, 240, 2)
display.text(f_bfree, 10, 40, 240, 2)
display.update()
  
while True:
    if display.is_pressed(display.BUTTON_X) and display.is_pressed(display.BUTTON_Y):
        display.set_pen(0, 0, 0)
        display.clear()
        display.set_pen(255, 0, 0)
        display.text("Rebooting..", 10, 10, 240, 2)
        display.update()
        time.sleep(0.1)
        machine.reset()
    time.sleep(0.1)

