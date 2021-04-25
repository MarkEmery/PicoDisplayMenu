
# Due to the Pico 2040 file system under Microphython being small, there's no file here by default
# If we can, load the background fast via the .IMG we save after converting the .BMP
try:
    restore = open("BACKGROUND.IMG", 'rb')
    restore.readinto(display_buffer)
    restore.close()
    display.update()
except OSError:  # .IMG open failed, convert the .BMP image
    try:
        image_file = open("BACKGROUND.BMP", 'rb') # Read, Binary.
        size = (os.stat("BACKGROUND.BMP")[6])
        bytes = size - 97200 # Skip past the header to leave 240 x 135 x 3 bytes for True Colour BMP.
        image_file = open("BACKGROUND.BMP", 'rb') # Read, Binary.
        image_file.seek(bytes) # Skip the header
    
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
        saveFile=open("BACKGROUND.IMG",'wb')
        saveFile.write(display_buffer)
        saveFile.close()
    except: 
        print("No file found")
        display.set_pen(0, 0, 0)
        display.clear()
        display.set_pen(255, 0, 0)
        display.text("No BACKGROUND.IMG file found.", 10, 10, 240, 2)
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
    utime.sleep(0.1)

