# -*- coding: UTF-8 -*-
import sys

import pygame
from pygame.locals import *


# 设置是否为开发模式，非开发时，需设置为False
DEBUG=True

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

gate = 0
current_gate = 0

def get_diffList(diffList):
    START_X, START_Y = WIDTH/2, PIC_HEIGHT
    #diffList = [(136, 259), (418, 219), (656, 180), (303, 375), (447, 395), (509, 350), (708, 319), (329, 513), (711, 552)]
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
    pygame.display.update

def check_for_quit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back

def get_game_time(diffList):
    if DEBUG:
        eachTime = 1
    else:
        eachTime = 10  # 每个10秒
    totalTmie = len(diffList) * eachTime
    return totalTmie
    
def check_for_click_on():
    '''
    return mouse click positoin (mouseX, mouseY)
    '''
    mouseX, mouseY = 0, 0
    for e in pygame.event.get():
        if e.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = e.pos
    return mouseX, mouseY

def click_on_yes_button_to_next():
    mouseX, mouseY = check_for_click_on() # get mouse position
    if(is_click_on_diff(mouseX, mouseY, [(635, 677)])): # click on yes
        gate += 0.5 
def prepare_for_gate(gate):
    ## 设置 
    current_gate = gate
    # 进入本关的坐标
    diffList = [(635, 677)]
    # set background
    set_bg_color(screen, BLUE)
    # add a picture as next button
    screen.blit(next, (0, 0)) 
    
    # loop
    while current_gate==gate:
        # load some text
        text = '第'+str(int(gate+0.5))+'关!'
        output_text(text, screen, (476, 483))
        # handle event
        check_for_quit()
        # 点击yes，设置gate+=0.5，进入下一关
        mouseX, mouseY = check_for_click_on() # 获取点击鼠标时候的位置
        if(is_click_on_diff(mouseX, mouseY, diffList)): # 判断该位置是否为yes按钮上
            gate= int(gate + 0.5)  
        pygame.display.update() # 显示准备进入第一关的图片

def runGame():
    global gate
    againHelp = 1
    running = True 
    gate = 0.4 # start from gate 0.4
    start_time = 0 #初始化每局游戏时间 
    frame_count = 0
    # game loop
    while running:
        ## 欢迎界面
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
                    gate = 0.5 
        ## 第一关准备
        elif gate==0.5 :
            current_gate = gate
            diffList = [(635, 677)]
            # set background
            set_bg_color(screen, BLUE)
            # add a picture as next button
            screen.blit(next, (0, 0)) 
            
            # loop
            while current_gate==gate:
                # load some text
                text = '第'+str(int(gate+0.5))+'关!'
                output_text(text, screen, (476, 483))
                # handle event
                check_for_quit()
                # 点击yes，设置gate+=0.5，进入下一关
                mouseX, mouseY = check_for_click_on() # 获取点击鼠标时候的位置
                if(is_click_on_diff(mouseX, mouseY, diffList)): # 判断该位置是否为yes按钮上
                    gate= int(gate + 0.5)  
                pygame.display.update() # 显示准备进入第一关的图片
        ## 进入第一关
        elif gate==1 :
            current_gate = gate
            ## 初始化设置
            # 初始化分数
            current_score = 0
            # 初始化游戏时间
            frame_count = 0
            # 不同点数据
            diffList = [(136, 259), (418, 219), (656, 180), (303, 375), (447, 395), (509, 350), (708, 319), (329, 513), (711, 552)]
            diffList = get_diffList(diffList)
            # 第一关的比较图片
            before = load_image("1.jpg")
            after = load_image("1.1.jpg")
            # 初始化背景为蓝色
            set_bg_color(screen, BLUE)
            # 添加比较图片到屏幕
            screen.blit(before, (BEFORE_X, PIC_HEIGHT))
            screen.blit(after, (START_X, START_Y))
            # 设置北京音乐
            clock_sound = pygame.mixer.Sound('clock.wav')
            clock_sound.play(-1) # -1 for loop forever until stoppting call
            # 设置本局游戏时间
            if (againHelp == 1):
                start_time = get_game_time(diffList)
                
            ## 游戏循环
            while gate==current_gate:
                ## 一些动画
                # 显示得分动画
                score = '得分: '+ str(current_score)
                output_text(score, screen, (WIDTH-150, 20))
                # 计算剩余时间
                left_seconds = start_time - (frame_count // FPS) #获取剩余时间
                if left_seconds < 0:
                    left_seconds = 0
                minutes = left_seconds // 60 
                seconds = left_seconds % 60
                # 显示剩余时间动画
                timeLeft = "剩余时间: {0:02}:{1:02}".format(minutes, seconds)
                output_text(timeLeft, screen, (WIDTH-500, 20))
                # 计算并显示剩余不同点个数
                diffLeft = '剩余个数: '+ str(len(diffList))
                output_text(diffLeft, screen, (WIDTH-300, 20))
                
                ## 如果时间用完，显示帮助提示
                if left_seconds == 0 :
                    clock_sound.stop() # 此时应该关闭钟表声音

                    # 如果提示次数已经用完，游戏结束，任意点击回到欢迎界面
                    if againHelp == 0: 
                        # 显示输了
                        text = '时间用完了，你输了！'
                        output_text(text, screen, (CENTER_X, CENTER_Y))
                        display_game_over(screen)
                        # 处理退出以及点击事件
                        check_for_quit()
                        mouseX, mouseY = check_for_click_on()
                        # 任意点击，退回欢迎界面
                        if (check_for_click_on()):
                            gate=0.4 
                    # 如果还有提示次数，询问其是否接受帮助
                    else:
                        # 刷新屏幕，以防止用户停在这里，观察不同点
                        screen.fill(BLUE)
                        # 显示是否需要提示
                        screen.blit(pygame.image.load('more_time.png'), (0,0))
                        
                        check_for_quit()
                        mouseX, mouseY = check_for_click_on()
                        # 如果用户接受帮助，重玩本关，进入本关欢迎界面
                        if(is_click_on_diff(mouseX, mouseY, [(557,673)])):
                            againHelp -= 1   # 减少帮助次数
                            if DEBUG:
                                start_time = get_game_time(diffList)
                            else:
                                start_time = get_game_time(diffList) * 2 # 为其增加游戏时间
                            gate = current_gate - 0.5      # 进入本关欢迎界面
                            #print(gate)
                        # 如果用户不接受帮助，点击cancle, 则退回至总欢迎界面
                        elif(is_click_on_diff(mouseX, mouseY, [(722, 675)])):
                            # go back to beginning
                            display_game_over(screen)
                            if (check_for_click_on()):
                                gate=0.4
                
                # 如果时间还有，则正常进行游戏
                else:
                    ## 
                    check_for_quit()   
                    mouseX, mouseY = check_for_click_on()
                    #如果点击点距离不同点比较近，则认为找到了不同点，标记圆圈
                    if(is_click_on_diff(mouseX, mouseY, diffList)): 
                        # 在点击点画圆
                        pygame.draw.circle(screen, RED, (mouseX, mouseY), RADIUS, 1)
                        #play_sound("right.wav")
                        # 分数加一
                        current_score += 1
                        # if all area are marked, succeed
                        # 如果全部不同点都找到，进入下一关
                    if len(diffList)==0:
                        gate = current_gate+0.5
                        print(gate) 
                
                # 记录一次循环次数（一帧次数）
                frame_count += 1
                #play_sound('clock.wav')
                # 按照FPS来设置一秒的循环次数
                clock.tick(FPS)              
                pygame.display.update()
             # 第一关循环结束后，关闭钟表声音。   
            clock_sound.stop()

        elif gate==1.5 :
            current_gate = gate
            diffList = [(635, 677)]
            # set background
            set_bg_color(screen, BLUE)
            # add a picture as next button
            screen.blit(next, (0, 0)) 
            
            # loop
            while current_gate==gate:
                # load some text
                text = '第'+str(int(gate+0.5))+'关!'
                output_text(text, screen, (476, 483))
                # handle event
                check_for_quit()
                # 点击yes，设置gate+=0.5，进入下一关
                mouseX, mouseY = check_for_click_on() # 获取点击鼠标时候的位置
                if(is_click_on_diff(mouseX, mouseY, diffList)): # 判断该位置是否为yes按钮上
                    gate= int(gate + 0.5)  
                pygame.display.update() # 显示准备进入第一关的图片
        ## 进入第一关
        elif gate==2 :
            ## 初始化设置
            # 初始化分数
            current_gate = gate
            current_score = 0
            # 初始化游戏时间
            frame_count = 0
            # 不同点数据
            diffList = [(105, 202), (368, 108), (712, 75),
                        (82, 340), (398, 397), (711, 492), 
                        (108, 715), (448, 658), (712, 232)]
            diffList = get_diffList(diffList)
            # 第一关的比较图片
            before = load_image(str(gate)+".jpg")
            after = load_image(str(gate)+".1.jpg")
            # 初始化背景为蓝色
            set_bg_color(screen, BLUE)
            # 添加比较图片到屏幕
            screen.blit(before, (BEFORE_X, PIC_HEIGHT))
            screen.blit(after, (START_X, START_Y))
            # 设置北京音乐
            clock_sound = pygame.mixer.Sound('clock.wav')
            clock_sound.play(-1) # -1 for loop forever until stoppting call
            # 设置本局游戏时间
            if (againHelp == 1):
                start_time = get_game_time(diffList)
                
            ## 游戏循环
            while current_gate==gate:
                ## 一些动画
                # 显示得分动画
                score = '得分: '+ str(current_score)
                output_text(score, screen, (WIDTH-150, 20))
                # 计算剩余时间
                left_seconds = start_time - (frame_count // FPS) #获取剩余时间
                if left_seconds < 0:
                    left_seconds = 0
                minutes = left_seconds // 60 
                seconds = left_seconds % 60
                # 显示剩余时间动画
                timeLeft = "剩余时间: {0:02}:{1:02}".format(minutes, seconds)
                output_text(timeLeft, screen, (WIDTH-500, 20))
                # 计算并显示剩余不同点个数
                diffLeft = '剩余个数: '+ str(len(diffList))
                output_text(diffLeft, screen, (WIDTH-300, 20))
                
                ## 如果时间用完，显示帮助提示
                if left_seconds == 0 :
                    clock_sound.stop() # 此时应该关闭钟表声音

                    # 如果提示次数已经用完，游戏结束，任意点击回到欢迎界面
                    if againHelp == 0: 
                        # 显示输了
                        text = '时间用完了，你输了！'
                        output_text(text, screen, (CENTER_X, CENTER_Y))
                        display_game_over(screen)
                        # 处理退出以及点击事件
                        check_for_quit()
                        mouseX, mouseY = check_for_click_on()
                        # 任意点击，退回欢迎界面
                        if (check_for_click_on()):
                            gate=0.4 
                    # 如果还有提示次数，询问其是否接受帮助
                    else:
                        # 刷新屏幕，以防止用户停在这里，观察不同点
                        screen.fill(BLUE)
                        # 显示是否需要提示
                        screen.blit(pygame.image.load('more_time.png'), (0,0))
                        
                        check_for_quit()
                        mouseX, mouseY = check_for_click_on()
                        # 如果用户接受帮助，重玩本关，进入本关欢迎界面
                        if(is_click_on_diff(mouseX, mouseY, [(557,673)])):
                            againHelp -= 1   # 减少帮助次数
                            if DEBUG:
                                start_time = get_game_time(diffList)
                            else:
                                start_time = get_game_time(diffList) * 2 # 为其增加游戏时间
                            gate=current_gate-0.5         # 进入本关欢迎界面
                        # 如果用户不接受帮助，点击cancle, 则退回至总欢迎界面
                        elif(is_click_on_diff(mouseX, mouseY, [(722, 675)])):
                            # go back to beginning
                            display_game_over(screen)
                            if (check_for_click_on()):
                                gate=0.4
                
                # 如果时间还有，则正常进行游戏
                else:
                    ## 
                    check_for_quit()   
                    mouseX, mouseY = check_for_click_on()
                    #如果点击点距离不同点比较近，则认为找到了不同点，标记圆圈
                    if(is_click_on_diff(mouseX, mouseY, diffList)): 
                        # 在点击点画圆
                        pygame.draw.circle(screen, RED, (mouseX, mouseY), RADIUS, 1)
                        #play_sound("right.wav")
                        # 分数加一
                        current_score += 1
                        # if all area are marked, succeed
                        # 如果全部不同点都找到，进入下一关
                        if len(diffList)==0:
                            gate = int(current_gate + 0.5) 
                
                # 记录一次循环次数（一帧次数）
                frame_count += 1
                #play_sound('clock.wav')
                # 按照FPS来设置一秒的循环次数
                clock.tick(FPS)              
                pygame.display.update()
             # 第一关循环结束后，关闭钟表声音。   
            clock_sound.stop()


def main():    
    runGame()

if __name__ == '__main__':
    main()
