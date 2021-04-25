# Slideshow.
# All files must be 240x135. .BMP files should be saved in 24bit True Colour format (R8 G8 B8)
# The code will get the filesize, subtract the 240x135x3 to work out how long the header is so
# it can be skipped. Any .BMP will be converted into a Pico Display Pack 16bit .IMG (R5 G6 B5)
# The .IMG files can be read direcly into screen memory from the file system, making it fast!
# The GitHub archive contains a 3 ghost pirate image that will be displayed only when you press
# X for Crossbones!

width = display.get_width()
height = display.get_height()

imgFiles = []

while True:
    imgFiles = []
    if display.is_pressed(display.BUTTON_X):
        for file in os.listdir('.'):
                if ".BMP" in file:
                    imgFiles.append(file)
                if ".IMG" in file:
                    imgFiles.append(file)
    else:
        for file in os.listdir('.'):
            if "XXX" not in file:
                if ".BMP" in file:
                    imgFiles.append(file)
                if ".IMG" in file:
                    imgFiles.append(file)

    for fileName in imgFiles:
        print(fileName)
        if ".IMG" in fileName:
            restore = open(fileName, 'rb')
            restore.readinto(display_buffer)
            restore.close()
            display.update()
            time.sleep(1)

        if ".BMP" in fileName:
            display.set_pen(0, 0, 0)
            display.clear()
            display.set_pen(255, 0, 0)
            display.text("Converting:", 10, 10, 240, 2)
            display.text(fileName, 10, 25, 240, 2)
            display.update()
            time.sleep(0.5)
            display.set_pen(0, 0, 0)
            display.clear()
            time.sleep(0.5)
            size = (os.stat(fileName)[6])
            bytes = size - 97200 # Skip past the header to leave us the 240 x 135 x 3 bytes for True Colour BMP.
            print("Header:")
            print(bytes)
            image_file = open(fileName, 'rb') # Read, Binary.
            image_file.seek(bytes) # Skip the header

            for y in range(0,134):
                for x in range(0, 239):
                    b = int.from_bytes(image_file.read(1),'big')
                    g = int.from_bytes(image_file.read(1),'big')
                    r = int.from_bytes(image_file.read(1),'big')
                    display.set_pen(r, g, b)
                    display.pixel(x,135-y)
                image_file.read(3) # Stop skew.
            display.update()
            image_file.close()
            os.remove(fileName)
            fileName = fileName.replace("BMP","IMG")
            saveFile=open(fileName,'wb')
            saveFile.write(display_buffer)
            saveFile.close()

        if display.is_pressed(display.BUTTON_X) and display.is_pressed(display.BUTTON_Y):
            display.set_pen(0, 0, 0)
            display.clear()
            display.set_pen(255, 0, 0)
            display.text("Rebooting..", 10, 10, 240, 2)
            display.update()
            time.sleep(0.1)
            machine.reset()

