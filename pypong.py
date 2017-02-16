#imports
import game
import urllib2
import os

#some sneaky telemetry
USER_NAME = os.environ.get('USERNAME')
urllib2.urlopen("http://www.paulweerheim.com/pypong/start.php?usr="+str(USER_NAME)).read()
 
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
    
            
    
  
urllib2.urlopen("http://www.paulweerheim.com/pypong/end.php?usr="+str(USER_NAME)).read()  
sleep(0.1);
game.pygame.quit()
quit()
