import os  # for OS calls
import pygame  # Import pygame graphics library
import RPi.GPIO as GPIO
import time
import subprocess
from pygame.locals import * #for event MOUSE variables


time_lim = 300
start_time=time.time()

run_flag=True
show_flag=False
global x,y
x,y=None,None

GPIO.setmode(GPIO.BCM)   # Set for GPIO (bcm) numbering not pin numbers...
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def quit_callback(channel):
    global run_flag
    run_flag=False


GPIO.add_event_detect(17,GPIO.FALLING, callback=quit_callback, bouncetime=300)

os.putenv('SDL_VIDEODRIVER', 'fbcon') # Display on piTFT
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV', 'TSLIB') # Track mouse clicks on PiTFT
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')


pygame.init()
pygame.mouse.set_visible(False)
WHITE=255,255,255
BLACK=0,0,0
size = width, height = 320, 240
screen = pygame.display.set_mode(size)

my_font=pygame.font.Font(None,30)
buttons1={'Mint':(160,60),'Succulent':(160,120),'Sanseviria':(160,180),'quit':(280,200)}
buttons2={'Back':(280,200)}
btn_size=20
screen.fill(BLACK)

buttons1_rect={} #create a rect dictionary
buttons2_rect={} #create a rect dictionary

for my_text,text_pos in buttons1.items():
    text_surface=my_font.render(my_text, True,WHITE)
    rect=text_surface.get_rect(center=text_pos)
    screen.blit(text_surface, rect)
    buttons1_rect[my_text]=rect # save rect for 'my-text' button
    
pygame.display.flip()


while (time.time()-start_time)<time_lim and run_flag:
    #my_clock.tick(FPS)
    screen.fill(BLACK)  # Erase the Work space
    if not show_flag:
        for event in pygame.event.get():
            if(event.type is MOUSEBUTTONDOWN):
                pos=pygame.mouse.get_pos()
            elif(event.type is MOUSEBUTTONUP):
                pos=pygame.mouse.get_pos()
                print(pos)
                x,y=pos
                if buttons1['quit'][0]-btn_size<=x<=buttons1['quit'][0]+btn_size and buttons1['quit'][1]-btn_size<=y<=buttons1['quit'][1]+btn_size:
                    run_flag=False
                if buttons1['Succulent'][0]-btn_size<=x<=buttons1['Succulent'][0]+btn_size and buttons1['succulent'][1]-btn_size<=y<=buttons1['Succulent'][1]+btn_size:
                    show_flag=True  #how to add different plants
        text="Touch at {}, {}".format(x,y)
        text_surface=my_font.render(text, True,WHITE)
        rect=text_surface.get_rect(center=(160, 120))
        screen.blit(text_surface, rect)
        # display menu 1
        for my_text,text_pos in buttons1.items():
            text_surface=my_font.render(my_text, True,WHITE)
            rect=text_surface.get_rect(center=text_pos)
            screen.blit(text_surface, rect)
            buttons1_rect[my_text]=rect # save rect for 'my-text' button
            
    if show_flag:
        # display menu 2
        for my_text,text_pos in buttons2.items():
            text_surface=my_font.render(my_text, True,WHITE)
            rect=text_surface.get_rect(center=text_pos)
            screen.blit(text_surface, rect)
            buttons2_rect[my_text]=rect # save rect for 'my-text' button
            for event in pygame.event.get():
                if(event.type is MOUSEBUTTONDOWN):
                    pos=pygame.mouse.get_pos()
                elif(event.type is MOUSEBUTTONUP):
                    pos=pygame.mouse.get_pos()
                    x,y=pos
                    
                if buttons2['Back'][0]-btn_size<=x<=buttons2['Back'][0]+btn_size and buttons2['Back'][1]-btn_size<=y<=buttons2['Back'][1]+btn_size:
                    show_flag=False
                    
            if show_flag:
                
    
        
    pygame.display.flip()
