# Display buffer is set up by main.py. We add the screen buffer and memory view

debug = 0

def get_pen(x,y):
    cursor = x * 2 + (y * width * 2)
    return mv[cursor] + mv[cursor + 1]

def check_background(a,b,dx,dy):
    x=int(a)
    y=int(b)
    test_x = 0
    test_y = 0
    if dx > 0:
        test_x = 2
    if dx < 0:
        test_x = -2
    if dy > 0:
        test_y = 1
    if dy < 0:
        test_y = -1
    colour_x = get_pen(x + test_x,          y)
    colour_y = get_pen(x,          test_y + y)
    colour_z = get_pen(x + test_x, test_y + y)
    # print(x,y,dx,dy,test_x,test_y,colour_x,colour_y)
    #
    #   O X   O    X   O
    #    \X   |  O-X    \
    #   XXX  XXX   X     X
    #
    if colour_z < 510 and colour_x == 510 and colour_y == 510:
        # Outer Corner Bounce
        return 3
    if colour_z < 510 and colour_x < 510 and colour_y < 510:
        # Inner Corner Bounce
        return 3
    elif colour_x < 510:
        return 1
    elif colour_y < 510:
        return 2
    return 0

# If we can, load the background fast via the .IMG we save after converting the .BMP
try:
    restore = open("SAVED.IMG", 'rb')
    restore.readinto(display_buffer)
    restore.close()
except OSError:  # .IMG open failed, convert the .BMP image
    image_file = open("IMG0-240x135.BMP", 'rb') # Read, Binary.
    # image_file.seek(138) # Skip the header # Normal RGB .BMP
    image_file.seek(24) # Skip the header # Normal RGB .BMP
    
    for y in range(0,134):
        image_file.read(3) # Stop skew.
        for x in range(0, 239):
            b = int.from_bytes(image_file.read(1),'big')
            g = int.from_bytes(image_file.read(1),'big')
            r = int.from_bytes(image_file.read(1),'big')
            display.set_pen(r, g, b)
            display.pixel(x,135-y)    
    display.update()
    image_file.close()
    saveFile=open("SAVED.IMG",'wb')
    saveFile.write(display_buffer)
    saveFile.close()

background.blit(screen_buffer,0,0,123) # Blit the display_buffer into the background frame buffer via the screen_buffer.

class Ball:
    def __init__(self, x, y, r, dx, dy, pen):
        self.x = x
        self.y = y
        self.r = r
        self.dx = dx
        self.dy = dy
        self.pen = pen

class Impact:
    def __init__(self, x, y, pen):
        self.x = x
        self.y = y
        self.pen = pen

# initialise shapes
balls = []
for i in range(0, 19):
    r = 3
    balls.append(
        Ball(
            20 + (i * 10),
            10,
            r,
            1,
            1,
            display.create_pen(255, 0, 0),
        )
    )

impacts = []

while True:
    screen_buffer.blit(background,0,0,123) # Blit our background into the display rather than clear the screen.
    for ball in balls:
        hit = 0
	if ball.x > 2 and ball.x < 238 and ball.y > 2 and ball.y < 133:
            hit = check_background(ball.x, ball.y, ball.dx, ball.dy)
	if hit > 0 and debug == 1:
            impacts.append(
                Impact(
                    int(ball.x),
                    int(ball.y),
                    display.create_pen(0, 255, 0),
                )
            )

        xmax = width - ball.r
        xmin = ball.r
        ymax = height - ball.r
        ymin = ball.r

        if hit == 3:
            ball.dx *= -1
            ball.dy *= -1
        elif hit == 1:
           ball.dx *= -1
        elif hit == 2:
            ball.dy *= -1
        elif ball.x < xmin or ball.x > xmax:
           ball.dx *= -1
        elif ball.y < ymin or ball.y > ymax:
            ball.dy *= -1

        ball.x += ball.dx
        ball.y += ball.dy

    for ball in balls:
        display.set_pen(ball.pen)
        display.circle(int(ball.x), int(ball.y), int(ball.r))

    for impact in impacts:
        display.set_pen(impact.pen)
        display.circle(impact.x, impact.y, 3)
        
    display.update()
    # time.sleep(0.2)
    if display.is_pressed(display.BUTTON_X) and display.is_pressed(display.BUTTON_Y):
        display.set_pen(0, 0, 0)
        display.clear()
        display.set_pen(255, 0, 0)
        display.text("Rebooting..", 10, 10, 240, 2)
        display.update()
        time.sleep(0.1)
	machine.reset()
