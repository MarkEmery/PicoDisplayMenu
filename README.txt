
Credits:
 Jungle Lander is based on code from SpiderMaf:
    https://github.com/SpiderMaf/PiPicoDsply/blob/main/junglelanderv2.py
    https://www.youtube.com/user/spidermaf
 All code based on initial code demos for the Pimoroni Pico Display Pack for the Raspbery Pi Pico RP2040

Ahoy!

Here's a menu system that'll allow you to keep lots of little programs on your Pico Display and pick
which to run.

The menu's main.py sets up:
 - the usual "display_buffer"
 - a "screen_buffer" pointer so we can blit into the screen
 - a "background" frame buffer to store a background image (see Pimoroni example)
 - a "mv" memory view so we can read from the display buffer to check pixel colours. This saves us from
   having to store image boundaries in an array. The data's in the buffer, just read it.

---- Main main.py init code ------8<----------------

width = display.get_width()
height = display.get_height()

display_buffer = bytearray(width * height * 2) # 2-bytes per pixel (RGB565)
display.init(display_buffer)
display.set_backlight(1.0)

# screen_buffer gives us a pointer so we can blit into our display_buffer.
screen_buffer = framebuf.FrameBuffer(display_buffer, width, height, framebuf.RGB565)
background = framebuf.FrameBuffer(bytearray(width * height * 2), width, height, framebuf.RGB565)
mv = memoryview(display_buffer)

----------------------------------8<----------------

Each Pico Display program should still be called main.py and live in a subdirectory.
Subdirectories must not contain a ".", only main.py and the directories should exist in /pyboard/

Comment out any display setup lines (like the ones between --8<-- above ) in the program to be called.
If they're left in, chances are you'll get an out-of-memory error. Make sure the code to be called is
using the same names display_buffer, screen_buffer, background, mv as and where needed.

In the program called, have this in the main while loop if possible:

        if display.is_pressed(display.BUTTON_X) and display.is_pressed(display.BUTTON_Y):
            display.set_pen(0, 0, 0)
            display.clear()
            display.set_pen(255, 0, 0)
            display.text("Rebooting..", 10, 10, 240, 2)
            display.update()
            time.sleep(0.1)
            machine.reset()

This will allow the user to exit the code with a XY press, not have to power-cycle or press a Captain Resetti
on the back. 

To debug a main.py in a subdirectory, run rshell, type repl<return> so you get the >>> prompt and paste in the
following, up to the exec line, changing "Slideshow" for your own sub-directory:

import time, random
import picodisplay as display
import utime
import gc
import os
import framebuf
import machine

width = display.get_width()
height = display.get_height()
display_buffer = bytearray(width * height * 2) # 2-bytes per pixel (RGB565)
display.init(display_buffer)
display.set_backlight(1.0)
screen_buffer = framebuf.FrameBuffer(display_buffer, width, height, framebuf.RGB565)
background = framebuf.FrameBuffer(bytearray(width * height * 2), width, height, framebuf.RGB565)
mv = memoryview(display_buffer)

os.chdir("Slideshow")
exec(open('main.py').read())

^^^ The exec should get the code running, all print() statements going to the console.

If you need help with the code, find me on @_MARKSE_ on Instagram or @_MARKSE on Twitter.

Enjoy! And try to pass the coding bug on. To a kid, if possible.
