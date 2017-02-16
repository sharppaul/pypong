#imports
import game
import urllib2
import os


# play song 
game.pygame.mixer.music.play(-1) 

ticktime = 1000.0/60.0;
lastupdate = game.pygame.time.get_ticks()

# main while loop
while not game.should_exit:
    if(game.pygame.time.get_ticks() - lastupdate > ticktime):
        game.update()
        lastupdate = game.pygame.time.get_ticks()
    game.draw()
    
            
game.pygame.quit()
quit()
