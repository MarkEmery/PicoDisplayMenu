

# reads from Pico's temp sensor and converts it into a more manageable number
sensor_temp = machine.ADC(4) 
conversion_factor = 3.3 / (65535) 

# Set the display backlight to 50%
display.set_backlight(0.5)
display.set_pen(0, 0, 0)
display.clear()

readings = []
for i in range(0, 239):
    readings.append(999)

i = 0

while True:

# the following two lines do some maths to convert the number from the temp sensor into celsius
    tempreading = sensor_temp.read_u16() * conversion_factor
    temperature = round(27 - (tempreading - 0.706) / 0.001721)    
    
    # Shift every value left 1 and add the new value
    dummy = readings.pop(0)
    readings.append(temperature)

    for i in range(0, 239):
        if readings[i] != 999:
            display.set_pen(0,0,0)
            display.rectangle(i, 0, 1, height - (readings[i] * 4))
            display.set_pen(0,255,0)
            if readings[i] > 20:
                display.set_pen(255,0,0)
            if readings[i] < 13:
               display.set_pen(0,0,255)
            display.rectangle(i, height - (readings[i] * 4), 1, height)
    
    # draws a white background for the text
    display.set_pen(0,255,0)
    if temperature > 20:
        display.set_pen(255,0,0)
    if temperature < 13:
        display.set_pen(0,0,255)
    
    display.rectangle(1, 1, 50, 25)
    
    # writes the reading as text in the white rectangle
    display.set_pen(0, 0, 0)
    display.text("{:.0f}".format(temperature) + "c", 3, 3, 0, 3)  
    # time to update the display
    display.update()
    
    # waits for 5 seconds
    utime.sleep(5)
    
    if display.is_pressed(display.BUTTON_X) and display.is_pressed(display.BUTTON_Y):
        display.set_pen(0, 0, 0)
        display.clear()
        display.set_pen(255, 0, 0)
        display.text("Rebooting..", 10, 10, 240, 2)
        display.update()
        time.sleep(0.1)
        machine.reset()
