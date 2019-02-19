# -*- coding: UTF-8 -*-

import pygame
import time

pygame.init()

## No FULL SCREEN
SCREENSIZE = (1280, 1204)
WIDTH, HEIGHT = SCREENSIZE
CENTER_X = WIDTH/2
CENTER_Y = HEIGHT/2
screen = pygame.display.set_mode(SCREENSIZE)

'''
## FULL SCREEN
SCREENSIZE = pygame.FULLSCREEN
screen = pygame.display.set_mode((0,0), SCREENSIZE)
displayInfo = pygame.display.Info()
WIDTH, HEIGHT = displayInfo.current_w, displayInfo.current_h
'''

## layout
PIC_HEIGHT = 80
START_X, START_Y = WIDTH/2, PIC_HEIGHT
BEFORE_X = 30

# fixed image
next = pygame.image.load("next.png")
# color
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (100, 100, 100)
# draw circle
RADIUS = 50

# timer
clock = pygame.time.Clock()
frame_count = 0
frame_rate = 20

def get_diffList(diffList):
    START_X, START_Y = WIDTH/2, PIC_HEIGHT
    diffList = [(136, 259), (418, 219), (656, 180), (303, 375), (447, 395), (509, 350), (708, 319), (329, 513), (711, 552)]
    before = 800
    after = 600
    scale = after/before
    diffList = [(int(x*scale+START_X), int(y*scale+START_Y)) for x,y in diffList]
    return diffList

def is_click_on_diff(mouseX, mouseY, diffList):
    '''
    click on any different area, return True
    '''
    offset = 50

    for index, (diffX, diffY) in enumerate(diffList):
        #print(diffX, diffY)
        if (diffX-offset < mouseX < diffX+offset and 
            diffY-offset < mouseY < diffY+offset):
            #pygame.draw.circle(screen, RED, (mouseX, mouseY), RADIUS, 1)
            diffList.remove(diffList[index])
            return True

def set_bg_color(screen, color):
    screen.fill(color)

def output_text(text, screen, posTuple):
    #text = str(text)
    fontObj = pygame.font.Font('FZLTHPro_GB18030_Zhun.otf', 32)
    textSurfaceObj = fontObj.render(text, True, GREEN, BLUE)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = posTuple
    screen.blit(textSurfaceObj, textRectObj)        

def play_sound(fileName):
    pygame.mixer.init(48000, -16, 1, 1024)
    soundObj = pygame.mixer.Sound(fileName)
    soundObj.play()
    while pygame.mixer.get_busy():
        pass

def load_image(name):
    name = str(name)
    img = pygame.image.load(name)
    img = pygame.transform.scale(img, (600, 600))
    return img


againHelp = 1

running = True
gate = 0.5
while running:
    ## GATE 0.5
    if gate==0.5 :
        # setup 
        # click position
        diffList = [(0,0)]
        # set background
        set_bg_color(screen, GRAY)
        # add a picture as next button
        screen.blit(next, (CENTER_X, CENTER_Y)) 
        # loop
        while gate==0.5:
            # load some text
            text = '来玩呀!'
            output_text(text, screen, (WIDTH/2-200, HEIGHT/2))
            # handle event
            for e in pygame.event.get():
                # check for exit event
                if e.type == pygame.KEYDOWN: # shutdown by keyboard pressed
                    gate=0
                    break
                # check for click on certain position
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    mouseX, mouseY = e.pos
                    if(is_click_on_diff(mouseX, mouseY, diffList)):
                        # enter next gate
                        gate = 1
                        break   
            pygame.display.update()
    ## GATE 1 
    elif gate==1 :
        # setup
        #init score
        current_score = 0
        #init frame_count
        frame_count = 0
        # different area position
        diffList = [(136, 259), (418, 219), (656, 180), (303, 375), (447, 395), (509, 350), (708, 319), (329, 513), (711, 552)]
        diffList = get_diffList(diffList)
        #image for gate 1
        before = load_image("1.jpg")
        after = load_image("1.1.jpg")
        #flush screen with color gray
        set_bg_color(screen, GRAY)
        #put image to screen
        screen.blit(before, (BEFORE_X, PIC_HEIGHT))
        screen.blit(after, (START_X, START_Y))
        #bg music
        clock_sound = pygame.mixer.Sound('clock.wav')
        clock_sound.play(-1) # -1 for loop forever until stoppting call
        # set gate time
        start_time = 5
        # loop
        while gate==1:
            ## some animate, like score, time.
            #show score animate
            score = '得分: '+ str(current_score)
            output_text(score, screen, (WIDTH-150, 20))
            #show left time animate
            total_seconds = start_time - (frame_count // frame_rate)
            if total_seconds < 0:
                total_seconds = 0
            minutes = total_seconds // 60
            seconds = total_seconds % 60
            timeLeft = "剩余时间: {0:02}:{1:02}".format(minutes, seconds)
            output_text(timeLeft, screen, (WIDTH-500, 20))
            # show left different area numbers
            diffLeft = '剩余个数: '+ str(len(diffList))
            output_text(diffLeft, screen, (WIDTH-300, 20))
            #pygame.display.update()
            # if time runs out
            if total_seconds == 0 :
                # stop clock music
                clock_sound.stop()
                # if there is no help left, fail.
                if againHelp == 0:
                    # show the user loosed.
                    text = '时间用完了，你输了！'
                    output_text(text, screen, (CENTER_X, CENTER_Y))
                    pygame.display.update()
                    for e in pygame.event.get():
                        #handle exit event
                        if e.type == pygame.KEYDOWN: # shutdown by keyboard pressed
                            gate=0
                            break
                        #handle click event
                        elif e.type == pygame.MOUSEBUTTONDOWN:
                            mouseX, mouseY = e.pos
                            #check if click on a dirrerent area
                            if(is_click_on_diff(mouseX, mouseY, diffList)): # if yes
                                gate=0 
                                break 
                    
                # ask for help 
                else:
                    #screen.fill((255,255,255,0))
                    text = '时间用完啦, 要重来一次嘛？'
                    output_text(text, screen, (CENTER_X, CENTER_Y))
                    #playAgain = load_image()
                    #screen.blit(playAgain, (BEFORE_X, PIC_HEIGHT))
                    for e in pygame.event.get():
                        if e.type == pygame.KEYDOWN: # shutdown by keyboard pressed
                            gate=0
                            #break
                        elif e.type == pygame.MOUSEBUTTONDOWN:
                            mouseX, mouseY = e.pos
                            # click certain area for ok
                            if(is_click_on_diff(mouseX, mouseY, [(0,0)])):
                                # go back to beginning
                                againHelp -= 1
                                gate=0.5
                                #break
            # if time doesn't run out
            else:
                ## handle event     
                for e in pygame.event.get():
                    #handle exit event
                    if e.type == pygame.KEYDOWN: # shutdown by keyboard pressed
                        gate=0
                        break
                    #handle click event
                    elif e.type == pygame.MOUSEBUTTONDOWN:
                        mouseX, mouseY = e.pos
                        #check if click on a dirrerent area
                        if(is_click_on_diff(mouseX, mouseY, diffList)): # if yes
                            # draw a circle to mark this area
                            pygame.draw.circle(screen, RED, (mouseX, mouseY), RADIUS, 1)
                            #play_sound("right.wav")
                            # increase score by 1
                            current_score += 1
                            # if all area are marked, succeed
                            if len(diffList)==0:
                                gate = 1.5
                                break
                        # if click on a wrong area, play a sound
                        else:
                            pass
                            #play_sound("wrong.wav")
                # show left different area
            
            # display update
            frame_count += 1
            #play_sound('clock.wav')
            clock.tick(frame_rate)              
            pygame.display.update()
        clock_sound.stop()
    else:
        running=False

# quit the game
pygame.quit()
