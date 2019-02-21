# -*- coding: UTF-8 -*-
import sys, random

import pygame
from pygame.locals import *


# 设置是否为开发模式，非开发时，需设置为False
DEBUG=False

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

total_diff_list = []

class Block(pygame.sprite.Sprite):
    """
    This class represents the ball
    It derives from the "Sprite" class in Pygame
    """
    def __init__(self, imgName, width, height):
        """ Constructor. Pass in the color of the block,
        and its x and y position. """
        # Call the parent class (Sprite) constructor
        super().__init__()
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        #self.image = pygame.Surface([width, height])
        #self.image.fill(color)
        
        self.image = pygame.image.load(imgName)
        self.image = pygame.transform.scale(self.image, (width, height))
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()
 
    def reset_pos(self):
        """ Reset position to the top of the screen, at a random x location.
        Called by update() or the main program loop if there is a collision.
        """
        self.rect.y = random.randrange(-300, -20)
        self.rect.x = random.randrange(0, WIDTH)
 
    def update(self):
        """ Called each frame. """
 
        # Move block down one pixel
        self.rect.y += 5
 
        # If block is too far down, reset to top of screen.
        if self.rect.y > HEIGHT:
            self.reset_pos()

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
    #while pygame.mixer.get_busy():
    #    pass

def load_image(name, width=600, height=600):
    name = str(name)
    img = pygame.image.load(name)
    img = pygame.transform.scale(img, (width, height))
    return img

def terminate():
    pygame.quit()
    sys.exit()

def check_for_quit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back

def get_game_time(num):
    if DEBUG:
        eachTime = 1
    else:
        eachTime = 10  # 每个10秒
    totalTmie = num * eachTime
    return totalTmie
    
def check_for_click_on():
    '''
    检查点击屏幕时间，并且返回鼠标点击位置
    '''
    mouseX, mouseY = 0, 0
    for e in pygame.event.get():
        if e.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = e.pos
    return mouseX, mouseY

def check_for_click():
    '''
    检查是否点击屏幕
    '''
    mouseX, mouseY = 0, 0
    for e in pygame.event.get():
        if e.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = e.pos
    if mouseX != 0:
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

def draw_circles(mouseX, mouseY, screen):
    # 右边图像的标记点
    pygame.draw.circle(screen, RED, (mouseX, mouseY), RADIUS, 1)
    # 计算左边图像的对应位置
    mouseX, mouseY = mouseX- 600, mouseY
    pygame.draw.circle(screen, GREEN, (mouseX, mouseY), RADIUS, 1)

def play_win_animate(play_seconds=5, FPS=25):
    # This is a list of 'sprites.' Each block in the program is
    # added to this list. The list is managed by a class called 'Group.'
    block_list = pygame.sprite.Group()
 
    # This is a list of every sprite. All blocks and the player block as well.
    all_sprites_list = pygame.sprite.Group()
 
    # 生成50张人民币
    for i in range(50):
        # This represents a block
        block = Block('renminbi.jpg', 150, 80)
     
        # Set a random location for the block
        block.rect.x = random.randrange(WIDTH)
        block.rect.y = random.randrange(HEIGHT)
     
        # Add the block to the list of objects
        block_list.add(block)
        all_sprites_list.add(block)


     
    # 设置屏幕刷新频率
    clock = pygame.time.Clock()
     
    # 设置运行时间
    frame_count = 0
    # 剩余时间
    left_seconds = 1
     
    #play_sound('hecai.wav')
    while (left_seconds):
        
        #检查退出时间
        check_for_quit()
        # Clear the screen
        screen.fill(BLUE)
     
        # Calls update() method on every sprite in the list
        all_sprites_list.update()
     
        all_sprites_list.draw(screen)
     
        # Limit to 20 frames per second
        clock.tick(FPS)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        #计算播放时间
        frame_count += 1

        left_seconds = play_seconds - (frame_count // FPS)
        #print(left_seconds)
        if left_seconds <0:
            left_seconds = 0

def play_lose_animate(FPS, screen):
    global againHelp, gate
    # 加载背景图片
    game_over_image = pygame.image.load("game_over.png")
    # 设置计时器
    clock = pygame.time.Clock()

    stay = True
    # 主循环中显示图片，检测退出和回到初始界面时间
    while stay:
        
        #检查退出时间
        check_for_quit()
        # 如果点击，退出游戏结束画面，并将入口设置为gate=0.4
        # 另外，将againHelp重置为1
        if(check_for_click()):
            stay=False
            againHelp = 1
            gate = 0.4
        # 显示图片
        screen.blit(game_over_image, (0,0))
        
        # 按FPS设定频率刷新显示器
        clock.tick(FPS)
        pygame.display.flip()

def set_total_diff_list():
    global total_diff_list
    total_diff_list = [
    # 第一关
    [(136, 259), (418, 219), (656, 180), 
     (303, 375), (447, 395), (509, 350), 
     (708, 319), (329, 513), (711, 552)],
    # 第二关
    [(105, 202), (368, 108), (712, 75),
     (82, 340), (398, 397), (711, 492), 
     (108, 715), (448, 658), (712, 232)],

    [(164, 152), (385, 172), (659, 218),
    (344, 619), (682, 654)],

    [(385, 63), (498, 131), (745, 144),
    (246, 241), (423, 324), (398, 536), (206, 613)],

    [(211, 147), (336, 134), (409, 139),
    (628, 120), (338, 395), (525, 473),
    (202, 604), (357, 591), (499, 603),
    (662, 612), (389, 723), (591, 718),
    (588, 780)],

    [(190, 75), (425, 112), (600, 105), 
    (215, 280), (422, 288), (603, 364), 
    (165, 596), (431, 663), (655, 611)],

    [(390, 229), (397, 339), (163, 412),
    (392, 409), (666, 437), (390, 533)],

    [(445, 476), (348, 592), (409, 646), 
    (580, 658), (202, 705), (300, 700)],

    [(204, 340), (1309, 326), (114, 254), 
    (292, 221), (378, 193), (473, 277), 
    (644, 268), (764, 298), (120, 377),
    (193, 393), (352, 373), (477, 391),
    (602, 429), (742, 435), (232, 491), 
    (277, 620), (240, 740), (70, 766), 
    (486, 488), (434, 604), (524, 716), (702, 665)],

    [(286, 69), (450, 54), (284, 146), (258, 194), 
    (313, 170), (470, 144), (273, 335), (385, 321),
    (417, 375), (522, 320), (590, 369), (270, 438), 
    (471, 435), (326, 559), (405, 630), (472, 602),
    (580, 631), (334, 707)],

    [(122, 233), (691, 126), (542, 428), 
    (708, 570), (369, 697), (703, 702)],

    [(204, 193), (598, 190), (295, 377), (101, 425), 
    (203, 512), (356, 542), (505, 403), (593, 536), 
    (684, 440), (406, 642), (656, 269)],

    # 第13关
    [(99, 246), (59, 388), (139, 508), (137, 671), 
    (281, 548), (466, 480), (493, 627), (740, 112), 
    (761, 300), (649, 384), (717, 507), (648, 571), 
    (689, 659)],

    #14
    [(207, 335), (409, 316), (618, 310), (314, 465), 
    (411, 436), (512, 443), (403, 616)],

    #15
    [(250, 113), (234, 190), (507, 176), (580, 265), 
    (576, 381), (234, 552), (533, 629)],

    #16
    [(428, 343), (240, 438), (628, 414), 
    (530, 496), (749, 501), (141, 575)],

    #17
    [(250, 406), (533, 228), (467, 354), 
    (490, 593), (698, 730)],

    #18
    [(372, 348), (260, 428), (301, 515), 
    (367, 492), (460, 494), (550, 426)],

    #19
    [(194, 352), (323, 352), (474, 278), (317, 579)],

    #20
    [(208, 257), (590, 253), (219, 519), (606, 515)],

    #21
    [(222, 392), (519, 373)],

    #22
    [(445, 160), (571, 152), (507, 286), (626, 285), 
    (452, 448), (630, 484), (554, 630)],

    #23
    [(152, 90), (273, 179), (411, 180), (568, 157), 
    (400, 260), (161, 413), (384, 424), (584, 376), 
    (215, 688), (385, 664), (573, 626)]  
    ]

def run_gate_pre(gate_num):
    global gate
    current_gate = gate_num
    diffList = [(635, 677)]
    # set background
    set_bg_color(screen, BLUE)
    # add a picture as next button
    screen.blit(next, (0, 0)) 
    
    # loop
    while current_gate==gate:
        # load some text
        text = '第'+str(current_gate+0.5)+'关!'
        output_text(text, screen, (476, 483))
        # handle event
        check_for_quit()
        # 点击yes，设置gate+=0.5，进入下一关
        mouseX, mouseY = check_for_click_on() # 获取点击鼠标时候的位置
        if(is_click_on_diff(mouseX, mouseY, diffList)): # 判断该位置是否为yes按钮上
            # 成功进入下一关
            gate= int(current_gate + 0.5)
            #print(gate)
        pygame.display.update() # 显示准备进入第一关的图片

def run_gate(gate_num, total_diff_list):
    global againHelp, gate, start_time
    current_gate = int(gate_num)
    ## 初始化设置
    # 初始化分数
    current_score = 0
    # 初始化游戏时间
    frame_count = 0
    # 不同点数据
    diffList =  total_diff_list[gate_num-1]   
    diffList = get_diffList(diffList)
    # different area num for get game time
    different_area_num = len(diffList)
    # 第一关的比较图片
    before = load_image(str(current_gate)+".jpg")
    after = load_image(str(current_gate)+".1.jpg")
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
        start_time = get_game_time(different_area_num)
        
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
                play_lose_animate(FPS, screen)

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
                        start_time = get_game_time(different_area_num)
                    else:
                        start_time = get_game_time(different_area_num) * 2 # 为其增加游戏时间
                    gate = current_gate - 0.5      # 进入本关欢迎界面
                    #print(gate)
                # 如果用户不接受帮助，点击cancle, 则退回至总欢迎界面
                elif(is_click_on_diff(mouseX, mouseY, [(722, 675)])): 
                    play_lose_animate(FPS, screen)
    
        
        # 如果时间还有，则正常进行游戏
        else:
            ## 
            check_for_quit()   
            mouseX, mouseY = check_for_click_on()
            #如果点击点距离不同点比较近，则认为找到了不同点，标记圆圈
            if(is_click_on_diff(mouseX, mouseY, diffList)): 
                # 在点击点画圆
                draw_circles(mouseX, mouseY, screen)
                #play_sound("right.wav")
                # 分数加一
                current_score += 1
                
                # 如果全部不同点都找到，进入下一关
            if len(diffList)==0:
                gate = current_gate+0.5
        
        # 记录一次循环次数（一帧次数）
        frame_count += 1
        #play_sound('clock.wav')
        # 按照FPS来刷新屏幕
        clock.tick(FPS)              
        pygame.display.update()
     # 第一关循环结束后，关闭钟表声音。   
    clock_sound.stop()

def run_game():
    global gate, againHelp, start_time, total_diff_list
    set_total_diff_list()

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
            run_gate_pre(gate)
        ## 进入第一关
        elif gate==1 :
            run_gate(gate, total_diff_list)
        elif gate==1.5 :
            run_gate_pre(gate)
        ## 进入第一关
        elif gate==2 :
            run_gate(gate, total_diff_list)
        elif gate==2.5:
            run_gate_pre(gate)
        elif gate==3:
            run_gate(gate, total_diff_list)
        elif gate==3.5:
            run_gate_pre(gate)
        elif gate==4:
            run_gate(gate, total_diff_list)
        elif gate==4.5:
            run_gate_pre(gate)
        elif gate==5:
            run_gate(gate, total_diff_list)
        elif gate==5.5:
            run_gate_pre(gate)
        elif gate==6:
            run_gate(gate, total_diff_list)
        elif gate==6.5:
            run_gate_pre(gate)
        elif gate==7:
            run_gate(gate, total_diff_list)
        elif gate==7.5:
            run_gate_pre(gate)
        elif gate==8:
            run_gate(gate, total_diff_list)
        elif gate==8.5:
            run_gate_pre(gate)
        elif gate==9:
            run_gate(gate, total_diff_list)
        elif gate==9.5:
            run_gate_pre(gate)
        elif gate==10:
            run_gate(gate, total_diff_list)
        # 10.5
        elif gate==10.5:
            run_gate_pre(gate)
        elif gate==11:
            run_gate(gate, total_diff_list)
        elif gate==11.5:
            run_gate_pre(gate)
        elif gate==12:
            run_gate(gate, total_diff_list)
        elif gate==12.5:
            run_gate_pre(gate)
        elif gate==13:
            run_gate(gate, total_diff_list)
        elif gate==13.5:
            run_gate_pre(gate)
        elif gate==14:
            run_gate(gate, total_diff_list)
        elif gate==14.5:
            run_gate_pre(gate)
        elif gate==15:
            run_gate(gate, total_diff_list)
        elif gate==15.5:
            run_gate_pre(gate)
        elif gate==16:
            run_gate(gate, total_diff_list)
        elif gate==16.5:
            run_gate_pre(gate)
        elif gate==17:
            run_gate(gate, total_diff_list)
        elif gate==17.5:
            run_gate_pre(gate)
        elif gate==18:
            run_gate(gate, total_diff_list)
        elif gate==18.5:
            run_gate_pre(gate)
        elif gate==19:
            run_gate(gate, total_diff_list)
        elif gate==19.5:
            run_gate_pre(gate)
        elif gate==20:
            run_gate(gate, total_diff_list)
        elif gate==20.5:
            run_gate_pre(gate)
        elif gate==21:
            run_gate(gate, total_diff_list)
        elif gate==21.5:
            run_gate_pre(gate)
        elif gate==22:
            run_gate(gate, total_diff_list)
        elif gate==22.5:
            run_gate_pre(gate)
        elif gate==23:
            run_gate(gate, total_diff_list)
        elif gate==23.5:
            run_gate_pre(gate)
        elif gate==24:
            run_gate(gate, total_diff_list)


        elif gate==24.5 :
            play_win_animate()

def main():
    run_game()
    #play_win_animate()

## 程序入口
if __name__ == '__main__':
    main()
