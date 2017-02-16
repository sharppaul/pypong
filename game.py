import sys
import pygame
import resources
import os


from random import randint
from pygame.locals import *

#pygame stuff
#initialize sound mixer
pygame.mixer.pre_init(44100, -16, 2, 2048)

#init game
pygame.init()

#get screen info
screeninfo = pygame.display.Info()

#set screen info
screen = pygame.display.set_mode((screeninfo.current_w,screeninfo.current_h), FULLSCREEN | DOUBLEBUF | HWSURFACE)

#set caption
pygame.display.set_caption('PyPong')

#load resources
pygame.display.set_icon(pygame.image.load(os.path.abspath("resources/pypong.png"))) #get ugly icon
pygame.mixer.music.load(os.path.join('resources', 'resistors.ogg')) #load music
button = pygame.mixer.Sound(os.path.join('resources','button.wav'))  #load sound
font = pygame.font.Font(os.path.abspath("resources/Pixeled.ttf"), 20) #load font

#set invis mouse
pygame.mouse.set_visible(False)

# game settings:

    #Points to win game. Player needs to have one more point than this to confirm the win, if both players get this much points, it's a draw.
POINTS_TO_WIN = 2
    #NPC chance to react every tick. (percentage)
NPC_CHANCE = 76
    #NPC range on screen to react. (percentage)
NPC_REACTION = 39 
    #Increase NPC bonus every X paddle hits
NPC_BONUS_INCREASE = 4

    #Player speed, increases slowly when ball gets faster
PLAYER_SPEED = 8
    #Increase player speed every X paddle hits
PLAYER_SPEED_INCREASE = 6
    #Player 2 hax
PLAYER_2_HACKS = False

    #Ball speed, increases gradually to max BALL_SPEED + 10
BALL_SPEED = 6
    #Increase ball speed every X paddle hits
BALL_SPEED_INCREASE = 6

# some variables

key = resources.Keyboard()

should_exit = False
game_state = resources.START
start_option = 0
pause_option = 0

key.w = False
key.s = False
key.up = False
key.down = False

width, height = pygame.display.get_surface().get_size()

ball = resources.Ball(width/2 - 10, height/2 + 56 - 10, 20, 20)
ball.has_started = False

score1 = 4
score2 = 4
game_done = False
ball_hits = 0

start_counter = 4
start_counted = False
multiplayer = False


# functions
def newPlayer(name, which):
    if which == 1:
        return resources.Player(name,30, (height/2)-20, 30,height/9)
        
    elif which == 2:
        return resources.Player(name,width-60,( height/2)-20, 30,height/9)
        
player1  = newPlayer("Player One", 1)
player2 = newPlayer("Player Two", 2)

def resetBall():
    global ball, start_counter, start_counted, ball_hits
    ball_hits = 0
    start_counter = 4
    start_counted = False
    ball = resources.Ball(width/2 - 10, height/2 + 56 - 10, 20, 20)
    ball.has_started = False
    
def resetGame():
    "resets settings to restart the game"
    global score1, score2, player1, player2, ball, start_counter, start_counted, game_done
    score1 = score2 = 0
    player1  = newPlayer("Player One", 1)
    player2 = newPlayer("Player Two", 2)
    game_done = False
    resetBall()

def startSingle():
    "starts single player"
    global multiplayer, game_state, player1, player2
    print("sp starting")
    
    resetGame()
    multiplayer = False
    player1  = newPlayer("Computer", 1)
    player2 = newPlayer("Player", 2)
    game_state = resources.PLAYING
    
def startMulti():
    "starts multiplayer"
    global multiplayer, game_state
    print("mp starting")
    
    resetGame()
    multiplayer = True
    game_state = resources.PLAYING
    
def keyDownEvent(kevent):
    global key, game_state, start_option, pause_option, should_exit, game_done
    if kevent.type == pygame.KEYDOWN:
        if kevent.key == pygame.K_w:
            key.w = True
        elif kevent.key == pygame.K_s:
            key.s = True
        elif kevent.key == pygame.K_UP:
            key.up = True
        elif kevent.key == pygame.K_DOWN:
            key.down = True
        
        elif kevent.key == pygame.K_p or kevent.key == pygame.K_ESCAPE:
            if game_state == resources.PLAYING: 
                game_state = resources.PAUSE
            elif game_state == resources.PAUSE:
                game_state = resources.PLAYING
                
        elif kevent.key == pygame.K_RETURN:
            if game_state == resources.PLAYING and game_done:
                game_state = resources.START
                resetGame()
                
            elif game_state == resources.START:
                button.play()
                if start_option == 0:
                    start_option = 0
                    resetGame()
                    startMulti()
                
                elif start_option == 1:
                    start_option = 0
                    resetGame()
                    startSingle()
                    
                elif start_option == 2:
                    game_state = resources.HELP
                elif start_option == 3:
                    should_exit = True
                    
            elif game_state == resources.PAUSE:
                button.play()
                if pause_option == 0:
                    pause_option = 0
                    game_state = resources.PLAYING
                elif pause_option == 1:
                    game_state = resources.START
                elif pause_option == 2:
                    should_exit = True
                    
            elif game_state == resources.HELP:
                button.play()
                game_state = resources.START

def keyUpEvent(kevent):
    global key
    if kevent.type == pygame.KEYUP:
        if kevent.key == pygame.K_w:
            key.w = False 
        elif kevent.key == pygame.K_s:
            key.s = False
        elif kevent.key == pygame.K_UP:
            key.up = False 
        elif kevent.key == pygame.K_DOWN:
            key.down = False
           
def updatePlayers():
    global player1, player2, ball, multiplayer, NPC_CHANCE, NPC_REACTION, PLAYER_2_HACKS, PLAYER_SPEED
    player1_change = 0
    player2_change = 0
    
    #player speed increases as the ball gets faster, to add more fun!
    px = PLAYER_SPEED 
    px += (ball_hits/PLAYER_SPEED_INCREASE) if (ball_hits/PLAYER_SPEED_INCREASE) < 10 else 10
    
    #to improve NPC when ball gets faster, to add more fair
    npc_bonus = (ball_hits/NPC_BONUS_INCREASE) if (ball_hits/NPC_BONUS_INCREASE) < 10 else 10
    
    #player 2 is always controllable, unless HAXORS are turned on!
    if PLAYER_2_HACKS:
        if ball.posy > player2.posy:
                player2_change -= px
        if ball.posy+ball.height < player2.posy+player2.height:
                player2_change += px
    else:
        if key.up:
            player2_change += px
        if key.down:
            player2_change -= px
    
    #if it's multiplayer, don't enable NPC (duh)
    if multiplayer:
        if key.w:
            player1_change += px
        if key.s:
            player1_change -= px
    
    #npc chances and settings are in the top of the file
    elif randint(1,100) <= (NPC_CHANCE + npc_bonus):
        if ball.posx < width * (float(NPC_REACTION + npc_bonus)/100.0):
            if ball.posy > player1.posy:
                player1_change -= px
            if ball.posy+ball.height < player1.posy+player1.height:
                player1_change += px
        
        else:
            if (height/2)-10 > player1.posy+(player1.height/2):
                player1_change -= px
                
            if (height/2)+10 < player1.posy+(player1.height/2):
                player1_change += px
    
        
        
    player1.posy -= player1_change
    player2.posy -= player2_change

    if player1.posy < 56:
        player1.posy = 56

    if player2.posy < 56:
        player2.posy = 56

    if player1.posy+player1.height > height:
        player1.posy = height - player1.height

    if player2.posy+player2.height > height:
        player2.posy = height - player2.height
        
def updateBall():
    global score1, score2, game_done, ball_hits
    
    spd = BALL_SPEED + (ball_hits/BALL_SPEED_INCREASE) if (ball_hits/BALL_SPEED_INCREASE) < 10 else 10
    ball.setSpeed(spd)
    
    ball.posy += ball.speedy 
    ball.posx += ball.speedx 
    
    if ball.posx < 0:
        score2 += 1
        print("score: ", score1, ":", score2)
        resetBall()
        
    if ball.posx + ball.width > width:
        score1 += 1
        print("score: ", score1, ":", score2)
        resetBall()
        
    if score2 > POINTS_TO_WIN or score1 > POINTS_TO_WIN or (score1 > POINTS_TO_WIN-1 and score2 > POINTS_TO_WIN-1):
        print("finalscore: ", score1, ":", score2)
        game_done = True
        
    if ball.posx <= player1.posx + player1.width and ball.posx > player1.posx:
        if ball.posy+ball.height > player1.posy and ball.posy < player1.posy+player1.height:
            if ball.getDirection() == ball.left_up():
                ball.setDirection(*ball.right_up())
            if ball.getDirection() == ball.left_down():
                ball.setDirection(*ball.right_down())
            ball_hits += 1
    
    if ball.posx + ball.width >= player2.posx and ball.posx + ball.width < player2.posx + player2.width:
        if ball.posy+ball.height > player2.posy and ball.posy < player2.posy+player2.height:
            if ball.getDirection() == ball.right_up():
                ball.setDirection(*ball.left_up())
            if ball.getDirection() == ball.right_down():
                ball.setDirection(*ball.left_down())
            ball_hits += 1
    
        
    if ball.posy <= 56:
        ball.posy = 56
        if ball.getDirection() == ball.right_up():
            ball.setDirection(*ball.right_down())
            
        if ball.getDirection() == ball.left_up():
            ball.setDirection(*ball.left_down())
    
    if ball.posy+ball.height >= height:
        ball.posy = height - ball.height
        if ball.getDirection() == ball.right_down():
            ball.setDirection(*ball.right_up())
            
        if ball.getDirection() == ball.left_down():
            ball.setDirection(*ball.left_up())
        
def drawPlayers():
    global screen, player1, player2
    screen.fill(resources.white, rect=player1.getRectangle())
    screen.fill(resources.white, rect=player2.getRectangle())
        
def drawBall():
    global screen, ball
    screen.fill(resources.white, rect=ball.getRectangle())  

def updateGame():
    """This function updates the game"""
    #adjust volume
    if pygame.mixer.music.get_volume()>0.5:
        pygame.mixer.music.set_volume(0.3)
    
    if not game_done and start_counter < 0:
        if not ball.has_started:
            ball.start()
        updatePlayers()
        updateBall()

def drawGame():
    """Draws the game components"""
    global start_counter, start_counted, game_done
    #draw start counter
    if start_counter > -1:
        if (pygame.time.get_ticks() / 400)%2 == 0:
            if not start_counted:
                start_counter -= 1
                start_counted = True
        else:
            start_counted = False
            
        if start_counter == 0:
            txtSurface = font.render("go!", True, resources.white, resources.black)
        else:
            txtSurface = font.render(str(start_counter), True, resources.white, resources.black)
        posx = width/2 - txtSurface.get_width()/2
        posy = height * 0.25     
        if start_counter > -1:
            screen.blit(txtSurface, (posx, posy))

    #draw if game done:
    if game_done:
        if score1 > POINTS_TO_WIN:
            txtSurface = font.render(player1.name+" won!", True, resources.white, resources.black)
        elif score2 > POINTS_TO_WIN:
            txtSurface = font.render(player2.name+" won!", True, resources.white, resources.black)
        elif score1 > POINTS_TO_WIN-1 and score2 > POINTS_TO_WIN-1:
            txtSurface = font.render("Draw!", True, resources.white, resources.black)
        
        posx = width/2 - txtSurface.get_width()/2
        posy = height * 0.25     
        screen.blit(txtSurface, (posx, posy))
        
        txtSurface = font.render("Press enter to continue...", True, resources.white, resources.black)
        posx = width/2 - txtSurface.get_width()/2
        posy = height * 0.45     
        screen.blit(txtSurface, (posx, posy))
    
    #scoregfx:
    txtSurface = font.render(str(score1)+':'+str(score2), True, resources.white, resources.black)
    posx = (width/2) - (txtSurface.get_width()/2)
    posy = 5      
    screen.blit(txtSurface, (posx, posy))
    
    #draw playernames and bar underneath:
    txtSurface = font.render(player1.name, True, resources.white, resources.black)
    posx = 5
    posy = 5      
    screen.blit(txtSurface, (posx, posy))
    
    txtSurface = font.render(player2.name, True, resources.white, resources.black)
    posx = width - txtSurface.get_width() - 5
    posy = 5      
    screen.blit(txtSurface, (posx, posy))
    
    posy += txtSurface.get_height()+5
    screen.fill(resources.white, rect=[0, posy, width, 5])
    
    if (pygame.time.get_ticks() / 300)%2 == 0 and ((score1 > POINTS_TO_WIN-1 or score2 > POINTS_TO_WIN-1) and (score2 <= POINTS_TO_WIN and score1 <= POINTS_TO_WIN)):
        txtSurface = font.render("Match Point!", True, resources.white)
        posx = (width/2) - (txtSurface.get_width()/2)
        posy += 10      
        screen.blit(txtSurface, (posx, posy))
        
    drawBall()
    drawPlayers()
 
def updatePause():
    "This function updates and renders the pause page"
    global pause_option, key
    #adjust music:
    if pygame.mixer.music.get_volume()<0.7:
        pygame.mixer.music.set_volume(0.7)
    
    #logic
    if key.up:
        button.play()
        key.up = False
        pause_option -= 1
        if pause_option < 0:
            pause_option = 2
        
    if key.down:
        button.play()
        key.down = False
        pause_option += 1
        if pause_option > 2:
            pause_option = 0
            
def drawPause():
    global screen, width, height
    #gfx
    titleSurface = font.render('Game Paused', True, resources.white, resources.black)
    titleEffectSurface = font.render('_', True, resources.white, resources.black)
    
    posx = (width/2) - (titleSurface.get_width()/2)
    posy = height * 0.25
    posx_effect = posx+titleSurface.get_width()
    
    screen.blit(titleSurface, (posx, posy))
    if (pygame.time.get_ticks() / 500)%2 == 0:
        screen.blit(titleEffectSurface, (posx_effect, posy))
        
    txtSelectedSurface = font.render('|', True, resources.white, resources.black)    
    
    #option 0
    txtSurface = font.render('resume', True, resources.white, resources.black)
    posx = (width/2) - (txtSurface.get_width()/2)
    posy = posy + 60  
    posy_effect = posy
    posx_effect = posx - txtSelectedSurface.get_width() - 5
    
    screen.blit(txtSurface, (posx, posy))
    
    #option 1
    txtSurface = font.render('stop playing', True, resources.white, resources.black)
    posx = (width/2) - (txtSurface.get_width()/2)
    posy += 35  
    
    if pause_option == 1:
        posx_effect = posx - txtSelectedSurface.get_width() - 5
        posy_effect = posy
    
    screen.blit(txtSurface, (posx, posy))
    
    #option 2
    txtSurface = font.render('quit game', True, resources.white, resources.black)
    posx = (width/2) - (txtSurface.get_width()/2)
    posy += 35  
    
    if pause_option == 2:
        posx_effect = posx - txtSelectedSurface.get_width() - 5
        posy_effect = posy
    
    screen.blit(txtSurface, (posx, posy))
    #selected char
    if (pygame.time.get_ticks() / 300)%3 != 0:
        screen.blit(txtSelectedSurface, (posx_effect,posy_effect))

def updateStart():
    """Updates logic in start menu"""
    global start_option, key
    #adjust music:
    if pygame.mixer.music.get_volume()<0.7:
        pygame.mixer.music.set_volume(0.7)
        
    #logic
    if key.up:
        button.play()
        key.up = False
        start_option -= 1
        if start_option < 0:
            start_option = 3
        
    if key.down:
        button.play()
        key.down = False
        start_option += 1
        if start_option > 3:
            start_option = 0
        
def drawStart():
    """This function draws the start menu"""
    global screen, width, height 
    
        
    #gfx
    titleSurface = font.render('PyPong', True, resources.white, resources.black)
    titleEffectSurface = font.render('_', True, resources.white, resources.black)
    
    posx = (width/2) - (titleSurface.get_width()/2)
    posy = height * 0.25
    posx_effect = posx+titleSurface.get_width()
    
    screen.blit(titleSurface, (posx, posy))
    if (pygame.time.get_ticks() / 500)%2 == 0:
        screen.blit(titleEffectSurface, (posx_effect, posy))
        
    txtSelectedSurface = font.render('|', True, resources.white, resources.black)    
    
    #option 0
    txtSurface = font.render('multiplayer', True, resources.white, resources.black)
    posx = (width/2) - (txtSurface.get_width()/2)
    posy = posy + 60  
    posy_effect = posy
    posx_effect = posx - txtSelectedSurface.get_width() - 5
    
    screen.blit(txtSurface, (posx, posy))
    
    #option 1
    txtSurface = font.render('singleplayer', True, resources.white, resources.black)
    posx = (width/2) - (txtSurface.get_width()/2)
    posy += 35  
    
    if start_option == 1:
        posx_effect = posx - txtSelectedSurface.get_width() - 5
        posy_effect = posy
    
    screen.blit(txtSurface, (posx, posy))
    
    #option 2
    txtSurface = font.render('help', True, resources.white, resources.black)
    posx = (width/2) - (txtSurface.get_width()/2)
    posy += 35  
    
    if start_option == 2:
        posx_effect = posx - txtSelectedSurface.get_width() - 5
        posy_effect = posy
    
    screen.blit(txtSurface, (posx, posy))
    
    #option 3
    txtSurface = font.render('quit game', True, resources.white, resources.black)
    posx = (width/2) - (txtSurface.get_width()/2)
    posy += 35  
    
    if start_option == 3:
        posx_effect = posx - txtSelectedSurface.get_width() - 5
        posy_effect = posy
    
    screen.blit(txtSurface, (posx, posy))
    
    #selected char
    if (pygame.time.get_ticks() / 300)%3 != 0:
        screen.blit(txtSelectedSurface, (posx_effect,posy_effect))
   
def drawHelp():
    "This function updates and renders the help page"
    global screen, width, height, key
    
    titleSurface = font.render('Help', True, resources.white, resources.black)
    titleEffectSurface = font.render('_', True, resources.white, resources.black)
    
    posx = (width/2) - (titleSurface.get_width()/2)
    posy = height * 0.25
    posx_effect = posx+titleSurface.get_width()
    posy_effect = posy
    
    screen.blit(titleSurface, (posx, posy))
    if (pygame.time.get_ticks() / 500)%2 == 0:
        screen.blit(titleEffectSurface, (posx_effect, posy_effect))
        
        
    txtSelectedSurface = font.render('|', True, resources.white, resources.black)    
    
    help = """This is the help page for PyPong. Play this game with UP+DOWN or W+S in multiplayer. Use RETURN to navigate."""
    
    credits = """Credits: Music by Erik Skiff. [ericskiff.com] Game made by Paul Weerheim. [paulweerheim.com]"""
    
    #option 0
    line = ""
    for word in help.split():
        line += word + " "
        if len(line) > 20:
            txtSurface = font.render(line, True, resources.white, resources.black)
            posx = (width/2) - (txtSurface.get_width()/2)
            posy = posy + 34
            screen.blit(txtSurface, (posx, posy))       
            line = ""
    
    if line != "":
        txtSurface = font.render(line, True, resources.white, resources.black)
        posx = (width/2) - (txtSurface.get_width()/2)
        posy = posy + 34
        screen.blit(txtSurface, (posx, posy))       
        line = ""
    
    
    posy += 20
    for word in credits.split():
        line += word + " "
        if len(line) > 20:
            txtSurface = font.render(line, True, resources.white, resources.black)
            posx = (width/2) - (txtSurface.get_width()/2)
            posy = posy + 34
            screen.blit(txtSurface, (posx, posy))       
            line = ""
            
    if line != "":
        txtSurface = font.render(line, True, resources.white, resources.black)
        posx = (width/2) - (txtSurface.get_width()/2)
        posy = posy + 34
        screen.blit(txtSurface, (posx, posy))       
        line = ""
    
    txtSurface = font.render('back', True, resources.white, resources.black)
    posx = (width/2) - (txtSurface.get_width()/2)
    posy = posy + 80
    screen.blit(txtSurface, (posx, posy))
    #selected char
    
    posy_effect = posy
    posx_effect = posx - txtSelectedSurface.get_width() - 5
    if (pygame.time.get_ticks() / 300)%3 != 0:
        screen.blit(txtSelectedSurface, (posx_effect,posy_effect))

def draw():
    """Render the rigth scene of the game"""
    global width, height
    screen.fill(resources.black)
    width, height = pygame.display.get_surface().get_size()
    if game_state == resources.START:
        drawStart()
    elif game_state == resources.HELP:
        drawHelp()
    elif game_state == resources.PAUSE:
        drawPause()
    elif game_state == resources.PLAYING:
        drawGame()    
    pygame.display.flip()
    
def update():
    """Updates the whole game"""
    global should_exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            should_exit = True
        elif event.type == pygame.KEYDOWN:
            keyDownEvent(event)
        elif event.type == pygame.KEYUP:
            keyUpEvent(event)
    if game_state == resources.START:
        updateStart()
    #elif game_state == resources.HELP:
        #updateHelp() Does not exist, not needed
    elif game_state == resources.PAUSE:
        updatePause()
    elif game_state == resources.PLAYING:
        updateGame()
  