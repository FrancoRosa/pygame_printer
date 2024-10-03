#!/usr/bin/env python
import io
import pygame
import rpc
import serial
import serial.tools.list_ports
import socket
import struct
import sys
from helpers import get_pdf, print_file 
from PIL import Image

interface = rpc.rpc_usb_vcp_master(port="/dev/ttyACM0")

width = 1280
height = 720
res = (width,height) 


def get_frame_buffer_call_back(pixformat_str, framesize_str, cutthrough, silent):
    if not silent:
        print("Getting Remote Frame...")

    result = interface.call("jpeg_image_snapshot", "%s,%s" %
                            (pixformat_str, framesize_str))
    if result is not None:

        size = struct.unpack("<I", result)[0]
        img = bytearray(size)

        if cutthrough:
            result = interface.call("jpeg_image_read")
            if result is not None:
                interface.get_bytes(img, 5000)  # timeout

        else:
            chunk_size = (1 << 15)

            if not silent:
                print("Reading %d bytes..." % size)
            for i in range(0, size, chunk_size):
                ok = False
                for j in range(3):  # Try up to 3 times.
                    result = interface.call(
                        "jpeg_image_read", struct.pack("<II", i, chunk_size))
                    if result is not None:
                        img[i:i+chunk_size] = result  # Write the image data.
                        if not silent:
                            print("%.2f%%" % ((i * 100) / size))
                        ok = True
                        break
                    if not silent:
                        print("Retrying... %d/2" % (j + 1))
                if not ok:
                    if not silent:
                        print("Error!")
                    return None

        return img

    else:
        if not silent:
            print("Failed to get Remote Frame!")

    return None


pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# colors
white = (255,255,255) 
gray = (170,170,170) 
dark = (100,100,100) 

smallfont = pygame.font.SysFont('Corbel',35) 
text = smallfont.render('Print!', True, white) 
text1 = smallfont.render('.. wait', True, white) 

bw = 100
bh = 40    
bx = round(width/2 - bw/2)
by = round(height - bh/2 - 100)


pygame.display.set_caption("IR Camera")
clock = pygame.time.Clock()

counter = 0
printing = False



while (True):
    if counter <= 0:
        printing=False
    else:
        counter = counter - 1
        printing = True
        
    sys.stdout.flush()
    img = get_frame_buffer_call_back(
        "sensor.RGB565", "sensor.QQVGA", cutthrough=True, silent=True)
    if img is not None:
        try:
            gameimage_jpg = pygame.image.load(io.BytesIO(img), "jpg")
            printerimage_jpg = im = Image.open(io.BytesIO(img))
            screen.blit(pygame.transform.scale(gameimage_jpg, (width, height)), (0, 0))
            mouse = pygame.mouse.get_pos()
            
            if bx <= mouse[0] <= bx+bw and by <= mouse[1] <= by+bh: 
                pygame.draw.rect(screen,gray,[bx,by,bw,bh]) 
                
            else: 
                pygame.draw.rect(screen,dark,[bx,by,bw,bh]) 
            
            screen.blit( text1 if printing else text , (bx + 15, by + 10)) 
            
            pygame.display.update()
            clock.tick()
        except pygame.error:
            pass

    # print(clock.get_fps()) //comented out to remove verbose

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                sys.exit()

            if event.key == pygame.K_SPACE:
                sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN: 
            if bx <= mouse[0] <= bx+bw and by <= mouse[1] <= by+bh: 
                if not printing:
                    print("... printing")
                    print(printerimage_jpg.size)
                    
                    get_pdf("/tmp/out.pdf", printerimage_jpg) 
                    print_file("/tmp/out.pdf")
                    counter = 20
                else:
                    print("...already printing")
                    
