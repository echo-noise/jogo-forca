import pygame
from pygame.locals import *
from core import *
from options import *
from sys import exit

class ScreenArea(object):
    def __init__(self, x, y, sizes):
        self.startx = x
        self.starty = y
        self.sizes = sizes

class Gallow(ScreenArea):
    def __init__(self):
        super().__init__(50, 100, (310, 120, 30))
        self.points = ((self.startx, self.starty + self.sizes[0]), (self.startx, 
                            self.starty), (self.startx + self.sizes[1], self.starty), 
                            (self.startx + self.sizes[1], self.starty + self.sizes[2]))

    def draw(self):
        pygame.draw.lines(BG, FGCOLOR, False, self.points, STROKE_WIDTH)
        
class Stickman(ScreenArea):
    def __init__(self, forca):
        super().__init__(forca.startx + forca.sizes[1], forca.starty 
                            + forca.sizes[2] + 2, (30, 40, 30, 20, 20, 40))
                     
    def draw_head(self):
        pygame.draw.circle(BG, FGCOLOR, ((self.startx  + round((STROKE_WIDTH / 2))), 
                            self.starty + round(self.sizes[0]/2)), 
                            round(self.sizes[0]/2), STROKE_WIDTH)

    def draw_body(self):
        starty = self.starty + self.sizes[0] - 1
        pygame.draw.line(BG, FGCOLOR, (self.startx, starty), (self.startx, 
                            starty + self.sizes[1]), STROKE_WIDTH)

    def draw_leftarm(self):
        starty = self.starty + self.sizes[0] + STROKE_WIDTH
        pygame.draw.line(BG, FGCOLOR, (self.startx, starty), (self.startx 
                            - self.sizes[2], starty + self.sizes[3]), STROKE_WIDTH)

    def draw_rightarm(self):
        starty = self.starty + self.sizes[0] + STROKE_WIDTH
        pygame.draw.line(BG, FGCOLOR, (self.startx, starty), (self.startx 
                            + self.sizes[2], starty + self.sizes[3]), STROKE_WIDTH)

    def draw_leftleg(self):
        starty = self.starty + self.sizes[0] + self.sizes[1]  
        pygame.draw.line(BG, FGCOLOR, (self.startx, starty), (self.startx 
                            - self.sizes[4], starty + self.sizes[5]), STROKE_WIDTH)

    def draw_rightleg(self):
        starty = self.starty + self.sizes[0] + self.sizes[1]  
        pygame.draw.line(BG, FGCOLOR, (self.startx, starty), (self.startx 
                            + self.sizes[4], starty + self.sizes[5]), STROKE_WIDTH)
    
    def update(self, damage):
        if damage == 1:
            self.draw_head()
        if damage == 2:
            self.draw_body()
        if damage == 3:
            self.draw_leftarm()
        if damage == 4:
            self.draw_rightarm()
        if damage == 5:
            self.draw_leftleg()
        if damage == 6:
            self.draw_rightleg()
        
class Playarea(ScreenArea):
    def __init__(self, font):
        super().__init__(90, 400, 50)
        self.indexes = []
        self.font = font

    def draw(self, n):
        x = self.startx
        for i in range(n):
            pygame.draw.rect(BG, FGCOLOR, (x, self.starty, self.sizes, STROKE_WIDTH))
            x += self.sizes + 5
            self.indexes.append(x)

    def update(self, found):
        for index, item in enumerate(found):
            if item != "0":
                txt = self.font.render(item.upper(), True, FGCOLOR)
                BG.blit(txt, (self.indexes[index] - FONTSIZE, self.starty 
                        - txt.get_rect().height + 5))
    
    def clear(self):
        self.indexes = []

class Guessarea(ScreenArea):
    def __init__(self, playarea, font):
        super().__init__(5, playarea.starty + 10, 
                            (BG.get_rect().width - 10, 180))
        self.font = font
        self.startcharx = 30
        self.startchary = self.starty + FONTSIZE
        self.charx = self.startcharx
        self.chary = self.startchary
        self.drawn = []

    def drawborder(self):
        pygame.draw.rect(BG, FGCOLOR, (self.startx, self.starty, self.sizes[0], 
                            self.sizes[1]), STROKE_WIDTH)

    def update(self, guesses):
        for item in guesses:
            if item not in self.drawn:
                self.drawn.append(item)
                txt = self.font.render(item.upper(), True, FGCOLOR)
                BG.blit(txt, (self.charx, self.chary))
                self.charx += txt.get_rect().width
                if self.charx >= BG.get_rect().width:
                    self.charx = self.startcharx
                    self.chary += txt.get_rect().height
    
    def clear(self):
        self.charx = self.startcharx
        self.chary = self.startchary
        self.drawn = []

class Button(object):
    def __init__(self, font, text, x, y):
        self.font = font
        self.text = self.font.render(text, True, FGCOLOR)
        self.width = self.text.get_rect().width + 3 * STROKE_WIDTH
        self.height = self.text.get_rect().height + 3 * STROKE_WIDTH
        self.x = x 
        self.y = y

    def draw(self):
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(BG, FGCOLOR, rect, BUTTON_BORDER)
        
        BG.blit(self.text, (rect.centerx - round(self.text.get_rect().width/2), 
                    rect.centery - round(self.text.get_rect().height)/2))

class Game(object):
    def __init__(self):
        self.name = ("forca")
        self.font = None
        self.font_small = None
        self.loadFont()
        self.core = Core()
        self.forca = Gallow()
        self.boneco = Stickman(self.forca)
        self.playarea = Playarea(self.font)
        self.guessarea = Guessarea(self.playarea, self.font)

    def loadFont(self):
        try:
            self.font = pygame.font.Font(FONTNAME, FONTSIZE)
            self.font_small = pygame.font.Font(FONTNAME_SMALL, FONTSIZE_SMALL)
        except OSError:
            self.font = pygame.font.Font(None, FONTSIZE)
            self.fonterrorscreen()

    def fonterrorscreen(self):
        message = "nao foi possivel carregar fonte"
        txt = self.font.render(message, True, FGCOLOR)
        BG.blit(txt, (BG.get_rect().centerx - round(txt.get_rect().width/2), 
                        BG.get_rect().centery))
        self.pygameupdate()

        while 1:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit(1)

    def endgame(self):
        if self.core.word == self.core.found:
            message = "VITORIA :)"
        else:
            message = "DERROTA :("

        txt = self.font.render(message, True, FGCOLOR)
        txt2 = self.font_small.render("jogar novamente?", True, FGCOLOR)

        ybutton = Button(self.font_small, "sim", BG.get_rect().centerx - 60, 
                            MSGY + txt.get_rect().height + txt2.get_rect().height + 5)
        nbutton = Button(self.font_small, "nao", ybutton.x + ybutton.width + 10, 
                            MSGY + txt.get_rect().height + txt2.get_rect().height + 5)
        
        ybutton.draw()
        nbutton.draw()
        BG.blit(txt, (BG.get_rect().centerx - (txt.get_rect().width/2), MSGY))
        BG.blit(txt2, (BG.get_rect().centerx - (txt.get_rect().width/2), 
                MSGY + (txt.get_rect().height/2) + 10))

        self.pygameupdate()
        while 1:
            mouse = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == QUIT:
                    exit(1)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if ybutton.width + ybutton.x > mouse[0] > ybutton.x and ybutton.height + ybutton.y > mouse[1] > ybutton.y: 
                        self.start()
                    if nbutton.width + nbutton.x > mouse[0] > nbutton.x and nbutton.height + nbutton.y > mouse[1] > nbutton.y: 
                        pygame.quit()


    def pygameupdate(self):
        SCREEN.blit(BG, (0,0))
        pygame.display.flip()
  
    def update(self):
        self.boneco.update(self.core.damage)
        self.playarea.update(self.core.found)
        self.guessarea.update(self.core.guessed)
        self.pygameupdate()

    def main(self):
        self.forca.draw()
        self.playarea.draw(len(self.core.word))
        self.guessarea.drawborder()

        SCREEN.blit(BG, (0,0))
        pygame.display.flip()

        while self.core.word != self.core.found and self.core.damage < self.core.maxdamage:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                if event.type == KEYDOWN:
                    self.core.read_input(event.unicode)

            self.update()
        self.endgame()

    def start(self):
        pygame.display.set_caption(self.name)
        BG.fill(BGCOLOR)
        self.core.reset()
        self.playarea.clear()
        self.guessarea.clear()
        self.main()
  
pygame.init()
SCREEN = pygame.display.set_mode(SCREENSIZE)
BG = pygame.Surface(SCREEN.get_size()).convert()

game = Game()
game.start()
