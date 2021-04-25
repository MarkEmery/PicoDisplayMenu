# Buffers set in main.py

width = display.get_width()
height = display.get_height()
max = 80
count = max

class Ball:
    def __init__(self, x, y, r, dx, dy, pen):
        self.x = x
        self.y = y
        self.r = r
        self.dx = dx
        self.dy = dy
        self.pen = pen

# initialise shapes
balls = []
for i in range(0, max):
    r = random.randint(0, 10) + 3
    red = int((14 - r) * 23);
    blue = int(r * 19.615);
    print("r: ", r, "Red: ", red, "Blue: ", blue);
    balls.append(
        Ball(
            random.randint(r, r + (width - 2 * r)),
            random.randint(r, r + (height - 2 * r)),
            r,
            (14 - r) / 2,
            (14 - r) / 2,
            display.create_pen(red, 0, blue),
        )
    )
    
while True:
    display.set_pen(0, 0, 0)
    display.clear()
    tc = 0
    for ball in balls:
        tc += 1
        if tc <= count:
            ball.x += ball.dx
            ball.y += ball.dy
            
            xmax = width - ball.r
            xmin = ball.r
            ymax = height - ball.r
            ymin = ball.r
    
            if ball.x < xmin or ball.x > xmax:
                ball.dx *= -1
    
            if ball.y < ymin or ball.y > ymax:
                ball.dy *= -1
    
            display.set_pen(ball.pen)
            display.circle(int(ball.x), int(ball.y), int(ball.r))
        
    display.update()
    time.sleep(0.01)
    if display.is_pressed(display.BUTTON_A):
       count += 1
       if count > max:
           count = max
       display.set_pen(0, 255, 0)
       display.text("{:.0f}".format(count), 10, 10, 240, 2)
       display.update()
       time.sleep(0.1)
    if display.is_pressed(display.BUTTON_B):
       count += -1
       if count < 1:
           count = 1
       display.set_pen(255, 0, 0)
       display.text("{:.0f}".format(count), 10, 10, 240, 2)
       display.update()
       time.sleep(0.1)
    if display.is_pressed(display.BUTTON_X) and display.is_pressed(display.BUTTON_Y):
        display.set_pen(0, 0, 0)
        display.clear()
        display.set_pen(255, 0, 0)
        display.text("Rebooting..", 10, 10, 240, 2)
        display.update()
        time.sleep(0.1)
        machine.reset()
    
