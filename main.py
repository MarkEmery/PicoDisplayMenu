
import time, random
import picodisplay as display
import utime
import gc
import os
import framebuf
import machine

# sets up a handy function we can call to clear the screen
def clear():  
    display.set_pen(0, 0, 0)
    display.clear()
    display.update()

def fill():
    display.set_pen(30, 30, 30)
    display.clear()
    display.update()

dirs = []
for dir in os.listdir('.'):
    if "." not in dir:
        dirs.append(dir)

num = len(dirs)
num = num - 1

width = display.get_width()
height = display.get_height()

display_buffer = bytearray(width * height * 2) # 2-bytes per pixel (RGB565)
display.init(display_buffer)
f = open("/brightness.val", "r")
brightness=float(f.read())
f.close()
display.set_backlight(brightness)

screen_buffer = framebuf.FrameBuffer(display_buffer, width, height, framebuf.RGB565) # A pointer so we can blit into our display_buffer.
background = framebuf.FrameBuffer(bytearray(width * height * 2), width, height, framebuf.RGB565)
mv = memoryview(display_buffer)

def update_menu():
    clear()
    offset = 0
    if item > 8:
      offset = item - 8
    display.set_pen(255, 255, 255)
    # display.text(str(item), 200, 14, 240, 2)
    # display.text(str(offset), 200, 28, 240, 2)
    
    for index in range(0,9): 
       if item == (offset+index):
           display.set_pen(0, 255, 0)
           display.rectangle(0, 14 * index, 239, 13)
           display.set_pen(0, 0, 0)
           text = "> " + dirs[offset+index]
       else:
           display.set_pen(255, 255, 255)
           text = "  " + dirs[offset+index]
       display.text(text, 10, 14 * index, 240, 2)
    display.update()
    utime.sleep(0.1)
    
item = 0
update_menu()

while True:
    if display.is_pressed(display.BUTTON_Y):              # if a button press is detected then...
        clear()                                           # clear to black
        display.set_pen(255, 255, 255)                    # change the pen colour
        display.text("Running..", 10, 10, 240, 2)         # display some text on the screen
        display.update()                                  # update the display
        utime.sleep(0.25)                                 # pause for a 1/2 a sec
        clear()                                           # clear to black again
        os.chdir(dirs[item])
        exec(open('main.py').read())
    elif display.is_pressed(display.BUTTON_A):
        item = item - 1
        if item == -1:
            item = num
        update_menu()                                     # clear to black
    elif display.is_pressed(display.BUTTON_B):
        item = item + 1
        if item > num:
            item = 0
        update_menu()                                     # clear to black
    utime.sleep(0.1)  # this number is how frequently the Pico checks for button presses

