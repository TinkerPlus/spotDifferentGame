# -*- coding: UTF-8 -*-
import sys

import pygame
from pygame.locals import *

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
BLUE = (0,1,124,0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (173, 173, 173)
# draw circle
RADIUS = 50

clock = pygame.time.Clock()
FPS = 25


def get_diffList(diffList):
    START_X, START_Y = WIDTH/2, PIC_HEIGHT
    diffList = [(136, 259), (418, 219), (656, 180), (303, 375), (447, 395), (509, 350), (708, 319), (329, 513), (711, 552)]
    before = 800
    after = 600
    scale = after/before
    diffList = [(int(x*scale+START_X), int(y*scale+START_Y)) for x,y in diffList]
    return diffList

def is_click_on_diff(mouseX, mouseY, diffList, offset=50):
    '''
    click on any different area, return True
    '''
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
    textSurfaceObj = fontObj.render(text, True, WHITE, BLUE)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = posTuple
    screen.blit(textSurfaceObj, textRectObj)        

def play_sound(fileName):
    pygame.mixer.init(48000, -16, 1, 1024)
    soundObj = pygame.mixer.Sound(fileName)
    soundObj.play()
    while pygame.mixer.get_busy():
        pass

def load_image(name, width=600, height=600):
    name = str(name)
    img = pygame.image.load(name)
    img = pygame.transform.scale(img, (width, height))
    return img

def play_sq():
    FPS = 10
    #imgList=['sq_0.png']
    # generate 7 png images' file name
    imgNamList = ['sq_'+str(num)+'.png' for num in range(7)]
    imgList = [pygame.image.load(name) for name in imgNamList]

    screen.blit(imgList[1], (0,0))
    time_passed = clock.tick()
    time_passed_seconds = time_passed / 1000
    pygame.display.update() 

#play_sq()

def terminate():
    pygame.quit()
    sys.exit()

def display_game_over(screen):
    img = pygame.image.load('game_over.png')
    screen.blit(img, (0,0))

def check_for_quit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back

def main():    
    runGame()
       
def check_for_click_on():
    '''
    return mouse click positoin (mouseX, mouseY)
    '''
    mouseX, mouseY = 0, 0
    for e in pygame.event.get():
        if e.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = e.pos
    return mouseX, mouseY


def runGame():
    againHelp = 1
    running = True 
    gate = 0.4 # start from gate 0.4
    start_time = 0 #ga 
    frame_count = 0
    # game loop
    while running:
        if gate == 0.4:
            # set background
            set_bg_color(screen, BLUE)
            screen.blit(pygame.image.load('shouye.png'), (0, 0)) 
            pygame.display.update()
            # loop
            while gate==0.4:           # start game 
                check_for_quit()
                mouseX, mouseY = check_for_click_on() # get mouse position
                if(is_click_on_diff(mouseX, mouseY, [(635, 677)])): # click on yes
                    # enter next gate
                    gate = 0.5 

        ## GATE 0.5
        elif gate==0.5 :
            # setup 
            # click position
            #diffList = [(0,0)]
            # set background
            set_bg_color(screen, BLUE)
            # add a picture as next button
            screen.blit(next, (0, 0)) 
            # loop
            while gate==0.5:
                # load some text
                text = '第一关!'
                output_text(text, screen, (476, 483))
                # handle event
                for e in pygame.event.get():
                    # check for exit event
                    if e.type == pygame.KEYDOWN: # shutdown by keyboard pressed
                        gate=0
                        break
                    # check for click on certain position
                    elif e.type == pygame.MOUSEBUTTONDOWN:
                        mouseX, mouseY = e.pos
                        if(is_click_on_diff(mouseX, mouseY, [(635, 677)])):
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
            set_bg_color(screen, BLUE)
            #put image to screen
            screen.blit(before, (BEFORE_X, PIC_HEIGHT))
            screen.blit(after, (START_X, START_Y))
            #bg music
            clock_sound = pygame.mixer.Sound('clock.wav')
            clock_sound.play(-1) # -1 for loop forever until stoppting call
            # set gate time
            start_time = 30
            # loop
            while gate==1:
                ## some animate, like score, time.
                #show score animate
                score = '得分: '+ str(current_score)
                output_text(score, screen, (WIDTH-150, 20))
                #show left time animate
                total_seconds = start_time - (frame_count // FPS)
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
                        display_game_over(screen)
                        #pygame.display.update()
                        for e in pygame.event.get():
                            #handle exit event
                            if e.type == pygame.KEYDOWN: # shutdown by keyboard pressed
                                gate=0
                                break
                            #handle click event
                            elif e.type == pygame.MOUSEBUTTONDOWN:
                                mouseX, mouseY = e.pos
                                #check if click on a dirrerent area
                                if(is_click_on_diff(mouseX, mouseY, [(556, 676)], 10)): # if yes
                                    gate=1 
                                elif(is_click_on_diff(mouseX, mouseY, [(722, 675)], 10)):
                                    display_game_over(screen)
                                    for e in pygame.event.get():
                                        #handle exit event
                                        if e.type == pygame.KEYDOWN: # shutdown by keyboard pressed
                                            gate=0
                                            break
                                        #handle click event
                                        elif e.type == pygame.MOUSEBUTTONDOWN:
                                            gate=0.4
                                            break
                        
                    # ask for help 
                    else:
                        screen.fill(BLUE)
                        #choose more time ?
                        screen.blit(pygame.image.load('more_time.png'), (0,0))
                        #playAgain = load_image()
                        #screen.blit(playAgain, (BEFORE_X, PIC_HEIGHT))
                        for e in pygame.event.get():
                            if e.type == pygame.KEYDOWN: # shutdown by keyboard pressed
                                gate=0
                                #break
                            elif e.type == pygame.MOUSEBUTTONDOWN:
                                mouseX, mouseY = e.pos
                                # click certain area for ok
                                if(is_click_on_diff(mouseX, mouseY, [(557,673)])):
                                    # go back to beginning
                                    againHelp -= 1
                                    start_time += 40

                                    gate=0.5
                                    break
                                elif(is_click_on_diff(mouseX, mouseY, [(722, 675)])):
                                    # go back to beginning
                                    display_game_over(screen)
                                    while(not pygame.event.get()):
                                        pass
                                    gate=0.4
                                    break
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
                clock.tick(FPS)              
                pygame.display.update()
            clock_sound.stop()
        else:
            running=False




if __name__ == '__main__':
    main()
