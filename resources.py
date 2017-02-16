from random import randint
white = (255,255,255)
black = (0,0,0)
red = (200,0,0)
grey = (100,100,100)

START = 0
PLAYING = 1
PAUSE = 2
HELP = 3

class Player:
    'Common base class for a player or AI'
    def __init__(self, name, posx, posy, width, height):
        self.name = name
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height

    def getRectangle(self):
        return [self.posx, self.posy, self.width, self.height]
        
class Ball:
    'Common base class for the ball'
    speed = 3
    def right_down(self): 
        return (self.speed, self.speed)    
    def right_up(self): 
        return (self.speed, -1 * self.speed)
    def left_down(self):
        return (-1 * self.speed, self.speed)   
    def left_up(self):
        return (-1 * self.speed, -1 * self.speed)
        
    def __init__(self, posx, posy, width, height):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height

    def getRectangle(self):
        return [self.posx, self.posy, self.width, self.height]
    
    def start(self):
        i = randint(1,4)
        if i == 4:
            self.setDirection(*self.right_down())
        elif i == 3:
            self.setDirection(*self.left_down())
        elif i == 2:
            self.setDirection(*self.right_up())
        elif i == 1:
            self.setDirection(*self.left_up())
        self.has_started = True
      
    def setDirection(self, speedx, speedy):
        self.speedx = speedx
        self.speedy = speedy
    
    def getDirection(self):
        return (self.speedx, self.speedy)
    
    def setSpeed(self, speed):   
        self.speed = speed
        if self.speedy < 0:
            self.speedy = -speed
        if self.speedx < 0:
            self.speedx = -speed
        if self.speedy > 0:
            self.speedy = speed
        if self.speedx > 0:
            self.speedx = speed
            
class Keyboard:
    'Class to keep track of key state'
    