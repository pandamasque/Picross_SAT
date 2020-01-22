import pygame as pg
from Picross import Picross_SAT
from Interface import Grid
from sys import exit



FPS = 30
WIDTH = 200
HEIGHT = 250
MIN = 5
MAX = 20
BACKGROUND_COLOR = (150,150,150)
TEXT_COLOR = (0,0,0)
BUTTON_COLOR = (255,255,255)



class Selection(object):


    def __init__(self):
        pg.init()
        pg.display.set_caption('Picross Selection') 
        self._screen = pg.display.set_mode((WIDTH,HEIGHT),flags=pg.DOUBLEBUF)
        self._font = pg.font.SysFont('Arial',200)
        self.size = MIN
        self._loop()


    def _loop(self):
        done = False
        clock = pg.time.Clock()
        while not done:
            clock.tick(FPS)
            self._drawMe()
            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.QUIT: 
                    done=True
                    break
                if event.type == pg.MOUSEBUTTONDOWN:
                    self._mouseClicHandeler()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_a:
                        done=True
                        break
        pg.quit()
        exit()



    def _drawMe(self):
        self._screen.fill(BACKGROUND_COLOR)

        text = self._font.render("Size", True, TEXT_COLOR) 
        text = pg.transform.smoothscale(text, (100, 30))
        self._screen.blit(text, (50, 10))
        pg.draw.rect(self._screen, BUTTON_COLOR, (50, 50, 100, 50))
        text = self._font.render("<", True, TEXT_COLOR) 
        text = pg.transform.smoothscale(text, (10, 50))
        self._screen.blit(text, (50, 50))
        text = self._font.render(">", True, TEXT_COLOR) 
        text = pg.transform.smoothscale(text, (10, 50))
        self._screen.blit(text, (140, 50))

        pg.draw.rect(self._screen, BUTTON_COLOR, (50, 150, 100, 50))
        text = self._font.render("START", True, TEXT_COLOR) 
        text = pg.transform.smoothscale(text, (100, 50))
        self._screen.blit(text, (50, 150))
       
        text = self._font.render(str(self.size), True, TEXT_COLOR) 
        text = pg.transform.smoothscale(text, (40, 30))
        self._screen.blit(text, (80, 60))
                    

    def _mouseClicHandeler(self):
        (x,y) = pg.mouse.get_pos()
            
        if x <= 60 and x>=50 and y >=50 and y <= 100:
            self.size = self.size - 1 if self.size > MIN else MIN
        elif x <= 150 and x>=140 and y >=50 and y <= 100:
            self.size = self.size + 1 if self.size < MAX else MAX
        elif x <= 150 and x>=50 and y >=150 and y <= 200:
            pg.quit()
            Grid(self.size, self.size, Picross_SAT)



