import pygame 

class Player(pygame.sprite.Sprite):
    '''This class defines the sprite for the player paddle. It creates the 
    paddle for two players and updates the positions when the paddle is moved.
    Hakd_paddle() will be called if half of the blocks have been destroyed
    to increase the difficulty. This will reset the position of the new 
    paddles to the center.'''
    def __init__(self,screen,player_num):
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        self.__number = player_num
        #Creating paddles based on player number
        if self.__number == 1:
            self.image = pygame.Surface((150,10))   
            self.image = self.image.convert()
            self.image.fill((0,148,249))
            self.rect = self.image.get_rect()
            self.rect.left = 1000/2 + 30
            self.rect.top = 630
        else:
            self.image = pygame.Surface((150,10))   
            self.image = self.image.convert()
            self.image.fill((230,0,230))
            self.rect = self.image.get_rect()
            self.rect.left = 1000/2 - 175   
            self.rect.top = 620
        self.__screen = screen
        self.__dx = 0
        
    def half_paddle(self):
        '''This method creates a new paddle that is half the size.'''
         #Creating paddles based on player number
        if self.__number == 1:
            self.image = pygame.Surface((75,10))   
            self.image = self.image.convert()
            self.image.fill((0,148,249)) 
            self.rect = self.image.get_rect()
            self.rect.left = 1000/2 + 10 
            self.rect.top = 630
        else:
            self.image = pygame.Surface((75,10))   
            self.image = self.image.convert()
            self.image.fill((230,0,230))
            self.rect = self.image.get_rect()
            self.rect.left = 1000/2 - 100  
            self.rect.top = 620 
        self.__dx = 0      
        
    def change_direction(self, xy_change):
        '''This method takes a (x,y) tuple as a parameter, extracts the 
        y element from it, and uses this to set the players y direction.'''
        self.__dx = xy_change[1]
    def update(self):
        '''This method will be called automatically to reposition the
        player sprite on the screen.'''      
        # Check if we have reached the top or bottom of the screen.
        # If not, then keep moving the player in the same x direction.
        if ((self.rect.left > 55) and (self.__dx > 0)) or\
           ((self.rect.right < 945) and (self.__dx < 0)):
            self.rect.left -= (self.__dx * 7)           
            
class Ball(pygame.sprite.Sprite):
    '''This class creates the ball. It reverses the direction according to
    the object it hits. The ball will also speed up whenever it hits a 
    paddle, adding difficulty to the game.'''
    def __init__(self,screen):
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)        
        
        self.image = pygame.Surface((30,30))
        self.image.fill((0,0,0))
        self.image.set_colorkey((0,0,0))
        pygame.draw.circle(self.image,(190,190,190),(15,15),15,0)
        self.rect = self.image.get_rect()
        self.rect.center = (screen.get_width() / 2, screen.get_height()/2)
        self.__screen = screen
        self.__dx = 5.5
        self.__dy = -5.5       
    def change_direction(self):
        '''This method causes the x direction of the ball to reverse.'''
        self.__dx = -self.__dx
        
    def change_hit(self):
        '''This method cause the y direction of the ball to reverse and 
        speeds up the ball.'''
        #Reverses direction if the ball is going up.'''
        if self.__dy >= 0:
            self.__dy = -self.__dy
        #Rereses direction and add speed if the ball is going down.'''
        else:
            self.__dy = -self.__dy + 0.1
            if self.__dx > 0:
                self.__dx = self.__dx + 0.1
            if self.__dx < 0:
                self.__dx = self.__dx - 0.1                
    def change_block_hit(self):
        '''Reverses the direction of the y axi.s'''
        self.__dy = -self.__dy           
    def update(self):
        '''This method will be called automatically to reposition the
        ball sprite on the screen.'''          
        # Check if we have reached the left or right end of the screen.
        # If not, then keep moving the ball in the same x direction.
        if ((self.rect.left > 55) and (self.__dx < 0)) or\
               ((self.rect.right < self.__screen.get_width() - 55) and \
                (self.__dx > 0)):
            self.rect.left += self.__dx
        # If yes, then reverse the x direction. 
        else:
            self.__dx = -self.__dx                 
        # Check if we have reached the top or bottom of the court.
        # If not, then keep moving the ball in the same y direction.
        if ((self.rect.top-65 > 0) and (self.__dy > 0)) or\
                ((self.rect.bottom+40 < self.__screen.get_height()) and \
                 (self.__dy < 0)):
            self.rect.top -= self.__dy
        # If yes, then reverse the y direction. 
        else:
            self.__dy = -self.__dy 
              
class Blocks(pygame.sprite.Sprite):
    '''This class accepts values as parameter to create the Blocks.'''
    def __init__(self,screen, color_list, from_top, from_left):
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self) 
        
        self.image = pygame.Surface((49,25))
        self.image.fill(color_list)
        self.rect = self.image.get_rect()
        self.rect.top = from_top
        self.rect.left = from_left
        self.__screen = screen
        self.__dx = 0
                
class EndZone(pygame.sprite.Sprite):
    '''This method sets the endzone so the ball can hit something.'''
    def __init__(self,screen):
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        y_position = 640
        self.image = pygame.Surface((screen.get_width(),5))
        self.rect = self.image.get_rect()
        self.rect.top = y_position
        self.rect.left = 0
          
class Lives(pygame.sprite.Sprite):
    '''This class keeps track of the lives that the player(s) have. It also
    displays the number of lives left.'''
    def __init__(self):
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self) 
        # Load our custom font, and initialize the starting lives.
        self.__font = pygame.font.Font("PonyMaker.ttf", 60)
        self.__lives = 5        
    def lost_life(self):
        '''This method subtracts lives from the count.'''
        self.__lives -= 0.5
    def add_life(self):
        '''This method adds a life when the white block is hit.'''
        self.__lives += 0.5   
    def get_life(self):
        '''This accessor method returns the number of lives a person has.'''
        return self.__lives    
    def update(self):
        '''This method updates the lives and displays it to the player(s).'''
        message = "  Lives  %d    " % self.__lives
        self.image = self.__font.render(message,1,(255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center =(300,30)
       
class ScoreKeeper(pygame.sprite.Sprite):
    '''This class defines a label sprite to display the score.'''
    def __init__(self):
        '''This initializer loads the system font "Arial", and
        sets the starting score to 0'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)       
        # Load our custom font, and initialize the starting score.
        self.__font = pygame.font.Font("PonyMaker.ttf", 60)
        self.__score = 0  
    def scored_points(self):
        '''This method adds 10 points when a regular block is hit.'''
        self.__score += 10            
    def scored_white(self):
        '''This method adds 50 points when the white block is hit.'''
        self.__Score += 50        
    def update(self):
        '''This method updates the score and displays it to the player(s).'''
        if self.__score <= 1:
            message = "    %d  Point    " % self.__score    
        else:    
            message = "    %d  Points  " % self.__score
        self.image = self.__font.render(message,1,(255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center = (660,30)
