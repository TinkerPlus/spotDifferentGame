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


## GATE 0.5
# setup 
gate = 0.5
diffList = [(0,0)]
set_bg_color(screen, GRAY)
screen.blit(next, (CENTER_X, CENTER_Y))


 
# loop
while gate==0.5:

    text = '来玩呀!'
    output_text(text, screen, (WIDTH/2-200, HEIGHT/2))

    for e in pygame.event.get():
        if e.type == pygame.KEYDOWN: # shutdown by keyboard pressed
            gate=0
            break
        elif e.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = e.pos
            if(is_click_on_diff(mouseX, mouseY, diffList)):
                gate = 1
                break   
    pygame.display.update()




## GATE 1 
if gate==1 :
    # setup
    current_score = 0
    diffList = [(136, 259), (418, 219), (656, 180), (303, 375), (447, 395), (509, 350), (708, 319), (329, 513), (711, 552)]
    diffList = get_diffList(diffList)
    #image
    before = load_image("1.jpg")
    after = load_image("1.1.jpg")


    set_bg_color(screen, GRAY)

    screen.blit(before, (BEFORE_X, PIC_HEIGHT))
    screen.blit(after, (START_X, START_Y))

    #bg music
    clock_sound = pygame.mixer.Sound('clock.wav')
    clock_sound.play(-1)

    # time left
    start_time = 5
    # loop
    while gate==1:
        ## some animate, like score, time.
        #score
        score = '得分: '+ str(current_score)
        output_text(score, screen, (WIDTH-150, 20))
        #time left
        total_seconds = start_time - (frame_count // frame_rate)
        if total_seconds < 0:
            total_seconds = 0
        minutes = total_seconds // 60
        seconds = total_seconds % 60

        timeLeft = "剩余时间: {0:02}:{1:02}".format(minutes, seconds)
        output_text(timeLeft, screen, (WIDTH-500, 20))
        
        ## handle event     
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN: # shutdown by keyboard pressed
                gate=0
                break
            elif e.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = e.pos
                if(is_click_on_diff(mouseX, mouseY, diffList)):
                    pygame.draw.circle(screen, RED, (mouseX, mouseY), RADIUS, 1)
                    #play_sound("right.wav")
                    current_score += 1
                    if len(diffList)==0: # success
                        gate = 1.5
                        break
                #else:
                    #play_sound("wrong.wav")
        # left
        diffLeft = '剩余个数: '+ str(len(diffList))
        output_text(diffLeft, screen, (WIDTH-300, 20))

        # display update
        frame_count += 1
        #play_sound('clock.wav')
        clock.tick(frame_rate)              
        pygame.display.update()


    clock_sound.stop()



## GATE 1.5

set_bg_color(screen, GRAY)
screen.blit(next, (0,0))
diffList = [(0,0)]

while gate==1.5:
    fontObj = pygame.font.Font('freesansbold.ttf', 32)
    textSurfaceObj = fontObj.render('You Find them! next gate...', True, GREEN, BLUE)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (200, 150)
    screen.blit(textSurfaceObj, textRectObj)

    for e in pygame.event.get():
        if e.type == pygame.KEYDOWN: # shutdown by keyboard pressed
            gate=0
            break
        elif e.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = e.pos
            if(is_click_on_diff(mouseX, mouseY, diffList)):
                gate=2
    pygame.display.update()


## GATE 2
if gate==2 :
    # setup
    current_score = 0
    diffList = [(105, 202), (368, 108), (712, 75),
                (82, 340), (398, 397), (711, 492), 
                (108, 715), (448, 658), (712, 232)]
    diffList = [(int(x+START_X), int(y+START_Y)) for x,y in diffList]
    #image
    before = pygame.image.load("2.jpg")
    after = pygame.image.load("2.1.jpg")
    set_bg_color(screen, GRAY)
    screen.blit(before, (0, PIC_HEIGHT))
    screen.blit(after, (START_X, START_Y))

    # loop
    while gate==2:
        #score
        score = 'Score: '+ str(current_score)
        output_text(score, screen, (WIDTH-150, 20))
        #time left
        total_seconds = start_time - (frame_count // frame_rate)
        if total_seconds < 0:
            total_seconds = 0
        minutes = total_seconds // 60
        seconds = total_seconds % 60

        timeLeft = "Time left: {0:02}:{1:02}".format(minutes, seconds)
        output_text(timeLeft, screen, (WIDTH-500, 20))
        
        #event
        '''
        if (total_seconds == 0):
            text = 'Your time running out!'
            output_text(text, screen, (WIDTH/2, HEIGHT/2))
            pygame.draw.circle(screen, RED, diffList.pop(), RADIUS, 1)
        
        else:
        ''' 
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN: # shutdown by keyboard pressed
                gate=0
                break
            elif e.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = e.pos
                if(is_click_on_diff(mouseX, mouseY, diffList)):
                    pygame.draw.circle(screen, RED, (mouseX, mouseY), RADIUS, 1)
                    play_sound("right.wav")
                    current_score += 1
                    if len(diffList)==0: # success
                        gate = 1.5
                        break
                else:
                    play_sound("wrong.wav")

        # left
        diffLeft = 'Left: '+ str(len(diffList))
        output_text(diffLeft, screen, (WIDTH-300, 20))

        # display update
        frame_count += 1
        clock.tick(frame_rate)          
        pygame.display.flip()

pygame.quit()
