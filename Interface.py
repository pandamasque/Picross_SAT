import pygame as pg
from Picross import Picross_SAT
import math
import numpy as np



FPS = 30
CELL_COLOR = (200,200,10)
BACKGROUND_COLOR = (0,0,0)
TEXT_COLOR = (0,0,0)
PANEL_COLOR = (0,150,0)
TEXT_ERROR_COLOR = (200,0,0)


class Grid(object):


    def __init__(self, size_x, size_y, picross):
        pg.init()
        pg.display.set_caption('Picross') 
        self._size_x = size_x
        self._size_y = size_y
        self._screen = pg.display.set_mode(flags=pg.DOUBLEBUF|pg.RESIZABLE)
        w, h = pg.display.get_surface().get_size()
        self._resize(w, h)
        self._font = pg.font.SysFont('Arial',200)
        self._picross = picross(size_x = size_x, size_y = size_y)
        self._contraint_x = np.zeros((size_x, math.ceil(size_y/2) + 1))
        self._contraint_y = np.zeros((size_y, math.ceil(size_x/2) + 1))
        self._solve()
        self._loop()
        self._solved = True


    def _defineCellSize(self):
        self._cellSize_x = self._width/(math.ceil(self._size_y/2) + self._size_x + 1)
        self._cellSize_y = self._height/(math.ceil(self._size_x/2) + self._size_y + 1)


    def _solve(self):
        try:
            self._picross.defineXConstraints(self._contraint_x.astype(int))
            self._picross.defineYConstraints(self._contraint_y.astype(int))
        except ValueError:
            self._solved = False
            return
        sol = self._picross.getSolution()
        if sol is None:
            self._solved = False
            return
        self._board = sol
        self._solved = True


    def _resize(self, w, h):
        self._width = w
        self._height = h
        self._defineCellSize()


    def _wipe(self):
        self._board = np.zeros((self._size_x, self._size_y))


    def _reset(self):
        self._contraint_x = np.zeros((self._size_x, math.ceil(self._size_y/2) + 1))
        self._contraint_y = np.zeros((self._size_y, math.ceil(self._size_x/2) + 1))
        self._solved = True
        self._wipe()


    def _loop(self):
        done = False
        clock = pg.time.Clock()
        while not done:
            clock.tick(FPS)
            self._drawMe()
            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.VIDEORESIZE:
                    self._resize(event.w, event.h)
                if event.type == pg.QUIT: 
                    done=True
                    break
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_s:
                        self._solve()
                    if event.key == pg.K_z:
                        self._wipe()
                    if event.key == pg.K_r:
                        self._reset()
                    if event.key == pg.K_a:
                        done=True
                        break
                if event.type == pg.MOUSEBUTTONDOWN:
                    self._mouseClicHandeler()
        from Selection import Selection
        pg.quit()
        Selection()


    def _getBoardValue(self,x,y):
        return 1-self._board[y,x]


    def _getColor(self, x, y):
        return (255*self._getBoardValue(x,y),255*self._getBoardValue(x,y),255*self._getBoardValue(x,y))


    def _drawValueConstraint(self, x, y, width, height, val):
        text = self._font.render(str(int(val)), True, TEXT_COLOR) 
        text = pg.transform.smoothscale(text, (int(width), int(height)))
        self._screen.blit(text, (x+1, y-1))


    def _drawMe(self):
        self._screen.fill(BACKGROUND_COLOR)
        pg.draw.rect(self._screen, PANEL_COLOR, (self._cellSize_x*self._size_x + 1, self._cellSize_y*self._size_y + 1, self._width - self._cellSize_x*self._size_x -2, self._height - self._cellSize_y*self._size_y -2))
        if not self._solved:
            text = self._font.render("No solution", True, TEXT_ERROR_COLOR) 
            text = pg.transform.smoothscale(text, (self._width - int(self._cellSize_x*self._size_x) -2, self._height - int(self._cellSize_y*self._size_y) -2))
            self._screen.blit(text, (self._cellSize_x*self._size_x + 1, self._cellSize_y*self._size_y + 1))
        for x in range(self._size_x):
            for y in range(self._size_y):
                pg.draw.rect(self._screen, self._getColor(x,y), (x*self._cellSize_x + 1, y*self._cellSize_y + 1, self._cellSize_x-2, self._cellSize_y-2))
        for x in range(math.ceil(self._size_x/2) + 1):
            for y in range(self._size_y):
                pg.draw.rect(self._screen, CELL_COLOR, ((self._size_x + x)*self._cellSize_x + 1, (y)*self._cellSize_y + 1, self._cellSize_x-2, self._cellSize_y-2))
                if self._contraint_y[y,x] >= 1:
                    self._drawValueConstraint((self._size_x + x)*self._cellSize_x , y*self._cellSize_y, self._cellSize_x-2, self._cellSize_y-2,self._contraint_y[y,x])
        for y in range(math.ceil(self._size_y/2) + 1):
            for x in range(self._size_x):
                pg.draw.rect(self._screen, CELL_COLOR, ((x)*self._cellSize_x + 1, (self._size_y + y)*self._cellSize_y + 1, self._cellSize_x-2, self._cellSize_y-2))
                if self._contraint_x[x,y] >=1 :
                    self._drawValueConstraint(x*self._cellSize_x, (self._size_y + y)*self._cellSize_y, self._cellSize_x-2, self._cellSize_y-2, self._contraint_x[x,y])
                    

    def _mouseClicHandeler(self):
        (x,y) = pg.mouse.get_pos()
        if pg.mouse.get_pressed()[0]:
            val = 1
        elif pg.mouse.get_pressed()[2]:
            val = -1
        else:
            return
            
        if (x > (self._size_x*self._cellSize_x)) and (x < self._width) and (y > 0) and (y < (self._cellSize_y*self._size_y)) :

            posx = int(x/self._cellSize_x) - self._size_x
            posy = int(y/self._cellSize_y)
            self._contraint_y[posy, posx] = ((self._contraint_y[posy, posx] + val) % (self._size_x+1))
            
        elif (x < (self._size_x*self._cellSize_x)) and (x > 0) and (y < self._height) and (y > (self._cellSize_y*self._size_y)) :

            posx = int(x/self._cellSize_x)
            posy = int(y/self._cellSize_y) - self._size_y
            self._contraint_x[posx, posy] = ((self._contraint_x[posx, posy] + val) % (self._size_y+1))



