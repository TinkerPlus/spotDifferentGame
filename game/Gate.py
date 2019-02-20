import pygame
import time
class Gate(object):
    def __init__(self, screen):
        self.screen = screen
        self.SCREEN_SIZE = (1280, 1204)
        self.WIDTH, self.HEIGHT = self.SCREEN_SIZE
        self.CENTER_X, self.CENTER_Y = self.WIDTH/2, self.HEIGHT/2


    def load_image(self, imgNamList):
        '''
        load image to the screen
        '''
        x, y = 
        img = pygame.image.load(img)
        img = pygame.transform.scale(img, (100, 100))
        self.screen.blit(img, (x, y))
        time.sleep(10)

    def update(self):
        pygame.display.update()

    def set_text(text, pos):
        pass

    def set_up():
        pass
    def loop():
        pass



import pygame

pygame.init()

SCREEN_SIZE = (400, 400)
screen = pygame.display.set_mode(SCREEN_SIZE)

gate1 = Gate(screen)
gate1.load_image('1.jpg', (0, 0))
gate1.update()

