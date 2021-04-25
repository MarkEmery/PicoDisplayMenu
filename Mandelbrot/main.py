
# Based on code from https://medium.com/swlh/visualizing-the-mandelbrot-set-using-python-50-lines-f6aa5a05cf0f

import math
import picodisplay as display

width = display.get_width()
height = display.get_height()

# Set the display backlight to 50%
display.set_backlight(0.5)
display.set_pen(0, 0, 0)
display.clear()
display.update()

#frame parameters
x = -0.65
y = 0
# xRange = 3.4 # Show full Mandlebrot
xRange = 3.2 # Zoomed in a bit
aspectRatio = width / height

precision = 50

yRange = xRange / aspectRatio
minX = x - xRange / 2
maxX = x + xRange / 2
minY = y - yRange / 2
maxY = y + yRange / 2

def sleep_clear():
    display.set_pen(0, 0, 0)
    display.clear()
    display.set_pen(0, 0, 180)
    display.text(str(minX), 10, 15, 240, 2)
    display.text(str(minY), 120, 15, 240, 2)
    display.text(str(maxX), 10, 35, 240, 2)
    display.text(str(maxY), 120, 35, 240, 2)
    display.update()
    time.sleep(0.5)
    while display.is_pressed(display.BUTTON_A) or display.is_pressed(display.BUTTON_B) or display.is_pressed(display.BUTTON_X) or display.is_pressed(display.BUTTON_Y):
        time.sleep(0.1)
    display.set_pen(0, 0, 0)
    display.clear()
    display.update()

def colorsys(h,s,v):
    h = float(h)
    s = float(s)
    v = float(v)
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0: r, g, b = v, t, p
    elif hi == 1: r, g, b = q, v, p
    elif hi == 2: r, g, b = p, v, t
    elif hi == 3: r, g, b = p, q, v
    elif hi == 4: r, g, b = t, p, v
    elif hi == 5: r, g, b = v, p, q
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return r, g, b

def logColor(distance, base, const, scale):
    color = -1 * math.log(distance, base)
    rgb = (const + scale * color,0.8,0.9)
    return tuple(round(i * 255) for i in rgb)

def powerColor(distance, exp, const, scale):
    color = distance**exp
    rgb = colorsys(const + scale * color, 1 - 0.6 * color, 0.9)
    return tuple(int(i) for i in rgb)

while True:
    reset = 0
    for x2 in range(0,5):
        if reset:
            break
        for y2 in range(0,5):
            if reset:
                break
            for row in range(0,height,5):
                if reset:
                    break
                for col in range(0,width,5):
                    if reset:
                        break
                    x = minX + (col+x2) * xRange / width
                    y = maxY - (row+y2) * yRange / height
                    oldX = x
                    oldY = y
                    for i in range(precision + 1):
                        a = x*x - y*y #real component of z^2
                        b = 2 * x * y #imaginary component of z^2
                        x = a + oldX #real component of new z
                        y = b + oldY #imaginary component of new z
                        if x*x + y*y > 4:
                            break
                    if i < precision:
                        distance = (i + 1) / (precision + 1)
                        rgb = powerColor(distance, 0.2, 0.27, 1.0)
                        display.set_pen(rgb[0],rgb[1],rgb[2])
                        display.pixel(col+x2, row+y2)
                display.update()
            
                if display.is_pressed(display.BUTTON_A) and display.is_pressed(display.BUTTON_X):
                    reset = 1
                    display.set_pen(255, 255, 255)
                    display.text("A+X Shift Left", 10, 10, 240, 2)
                    display.update()
                    time.sleep(0.5)
                    minX = minX + 0.1
                    maxX = maxX + 0.1
                    sleep_clear()
                elif display.is_pressed(display.BUTTON_A) and display.is_pressed(display.BUTTON_Y):
                    reset = 1
                    display.set_pen(255, 255, 255)
                    display.text("B+X Shift Right", 10, 25, 240, 2)
                    display.update()
                    time.sleep(0.5)
                    minX = minX - 0.1
                    maxX = maxX - 0.1
                    sleep_clear()
                elif display.is_pressed(display.BUTTON_B) and display.is_pressed(display.BUTTON_X):
                    reset = 1
                    display.set_pen(255, 255, 255)
                    display.text("A+Y Shift Up", 10, 40, 240, 2)
                    display.update()
                    time.sleep(0.5)
                    # Shift Up 
                    minY = minY - 0.1
                    maxY = maxY - 0.1
                    sleep_clear()
                elif display.is_pressed(display.BUTTON_B) and display.is_pressed(display.BUTTON_Y):
                    reset = 1
                    display.set_pen(255, 255, 255)
                    display.text("B+Y Shift Down", 10, 55, 240, 2)
                    display.update()
                    time.sleep(0.5)
                    minY = minY + 0.1
                    maxY = maxY + 0.1
                    sleep_clear()
                elif display.is_pressed(display.BUTTON_X) and display.is_pressed(display.BUTTON_Y):
                    display.set_pen(0, 0, 0)
                    display.clear()
                    display.set_pen(255, 255, 255)
                    display.text("Rebooting..", 10, 10, 240, 2)
                    display.update()
                    time.sleep(0.1)
                    machine.reset()
                elif display.is_pressed(display.BUTTON_X):
                    reset = 1
                    display.set_pen(255, 255, 255)
                    display.text("X Zoom In", 10, 70, 240, 2)
                    display.update()
                    time.sleep(0.5)
                    minX = minX + 0.1
                    maxX = maxX - 0.1
                    minY = minY + 0.1
                    maxY = maxY - 0.1
                    sleep_clear()
                elif display.is_pressed(display.BUTTON_Y):
                    reset = 1
                    display.set_pen(255, 255, 255)
                    display.text("Y Zoom Out", 10, 85, 240, 2)
                    display.update()
                    time.sleep(0.5)
                    minX = minX - 0.1
                    maxX = maxX + 0.1
                    minY = minY - 0.1
                    maxY = maxY + 0.1
                    sleep_clear()

 
