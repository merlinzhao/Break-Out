'''
Author: Merlin Zhao

***REUIRED: Python 2.7, pygame 1.9.1 for python 2.7***
This is a version of the popular game Super BreakOut. This is a two
player game(leave player 2 idle if only one player). There are 108 bricks + 1
special white bricks to be demolished. Eliminate all to win! The paddle will
reduce in size after 60 bricks are gone so beware! This game has three 
different songs as background music and is selected randomly when you start
the same. The song's album art work is displayed in the lower right corner.
Enjoy the game!
*** Controls ***
left and right arrow keys for palyer 1 (blue)
a and d keys or up down on the joy stick for player 2 (pink)
esc - end game
space - starts the game
'''
import pygame, breakSprites, random
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1000, 680))

#List of Joystick objects.
joysticks = []
for joystick_no in range(pygame.joystick.get_count()):
    stick = pygame.joystick.Joystick(joystick_no)
    stick.init()
    joysticks.append(stick)
    
def main():
    '''This function defines the 'mainline logic' for the game.'''
    #DISPLAY
    pygame.display.set_caption("Super Break-Out")
    
    #ENTITIES
    #the white background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0,0,0))
    screen.blit(background, (0, 0)) 
    
    #Game font
    message_font = pygame.font.Font("PonyMaker.ttf", 100)
    message = message_font.render("Game Over",1,(255,100,0))
    
    #Intro page font
    page_font = pygame.font.SysFont("Arial",17)
    page_message_one = page_font.render("Objective: Eliminate all the blocks\
!",1,(255,255,255))
    page_message_two = page_font.render("Player 1: Arrow Keys      \
Player 2: A and D Keys or Joystick",1,(255,255,255))
    page_message_three = page_font.render("You have 5 lives. Eliminate the \
white block for a bonus life and 50 points",1,(255,255,255))
    page_message_four = page_font.render("Hit the Space Bar to begin your \
journey!",1,(255,255,255))
    page_warning = page_font.render("The ball's speed will increase and if \
you're unlucky, the paddle size will be halfed!" ,1,(255,255,255))    
    page_warningtwo = page_font.render("You have been warned." ,1,(255,255,255)) 

    #wallpaper
    wallpaper = pygame.image.load("wallpaper.gif")
    wallpaper.convert()
    screen.blit(wallpaper,(0,0))    
    
    #Game sounds
    winner_sound = pygame.mixer.Sound("Winner.wav")
    winner_sound.set_volume(0.5)
    hit_sound = pygame.mixer.Sound("Ding.wav")
    hit_sound.set_volume(1.0)
    error_sound = pygame.mixer.Sound("beep.wav")
    error_sound.set_volume(0.3)
    fail_sound = pygame.mixer.Sound("Fail.wav")
    fail_sound.set_volume(0.8)
    
    #background music + artwork
    choose_music = random.randrange(3)
    if choose_music == 0:
        pygame.mixer.music.load("Sound.wav")
        album_art = pygame.image.load("sound.png")
    if choose_music == 1:
        pygame.mixer.music.load("Stars.wav")
        album_art = pygame.image.load("stars.png")
    if choose_music == 2: 
        pygame.mixer.music.load("Firework.mp3")
        album_art = pygame.image.load("firework.png")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)
    album_art.convert()
    
    #Instruction
    instro_font = pygame.font.SysFont("Arial",11)
    intro = instro_font.render("Objective: Eliminate all the blocks! Player \
1 use the arrow keys and Player 2 use the 'a' and 'd' keys or a joystick. \
Hit the white block for a bonus life and 50 points!",1,(200,200,200))
    
    #Sprites for:
    player1 = breakSprites.Player(screen,1)
    player2 = breakSprites.Player(screen,2)
    ball = breakSprites.Ball(screen)
    lives_keeper = breakSprites.Lives()
    endzone = breakSprites.EndZone(screen)
    block = breakSprites
    score_keeper = breakSprites.ScoreKeeper()
    
    #Thi list is used to keep track of how many blocks disappear
    blocks_hit_list = []
    #create the special white block worth 50 points and adds a life.  
    #It will only appear in the red and pink rows.
    from_left_white = random.randrange(18)
    from_top_white = random.randrange(0,2)  
    the_blocks_whiteone = []
    for blocks in range(1):
        from_left_white = 9 + (49 * (from_left_white+1))
        from_top_white = 67 + (29 * from_top_white)
        the_blocks_whiteone.append(block.Blocks(screen,(230,230,230),\
                                            from_top_white,from_left_white))  
    white_block = pygame.sprite.Group(the_blocks_whiteone)
    
    #Creating all the blocks.
    color_list = [(255,50,220),(250,50,50),(255,118,0),(255,250,0),(0,255,90)\
                  ,(0,128,255)]

    from_top = 38
    blocks_list = [] 
    #First create the rows
    for blocks in range(6):
        from_top += 29
        from_left = 9
        #Then create colums
        for left in range(18):
            from_left += 49
            blocks_list.append(block.Blocks(screen,color_list[blocks],\
                                            from_top,from_left))
    blocks_group = pygame.sprite.Group(blocks_list)    

    #Grouping all sprites in order to be displayed 
    allSprites = pygame.sprite.OrderedUpdates(player1,player2,ball,\
        lives_keeper, score_keeper, endzone,blocks_list,the_blocks_whiteone)
    
    #ACTION
    #ASSIGN
    clock = pygame.time.Clock()
    keepGoing = True
    displayIntro = True
    
    # Hide the mouse pointer
    pygame.mouse.set_visible(False)   
    
    #THIS LOOP IS FOR THE INTRO PAGE.
    while keepGoing and displayIntro:
        #TIME
        clock.tick(60)   
        
        #EVENT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False    
            elif event.type == pygame.KEYDOWN:    
                if event.key == pygame.K_SPACE:
                    displayIntro = False
                elif event.key == pygame.K_ESCAPE:
                    keepGoing = False                      
        title = message_font.render("Super Breakout",1,(0,220,255))
        #REFRESH
        screen.blit(title,(83,30))
        screen.blit(album_art,(815,510))
        screen.blit(page_message_one,(370,160))
        screen.blit(page_message_two,(280,240))
        screen.blit(page_message_three,(215,280))
        screen.blit(page_warning,(185,420))
        screen.blit(page_warningtwo,(415,460))
        screen.blit(page_message_four,(350,510))
        pygame.display.flip()
    
    #LOOP FOR THE GAME
    while keepGoing:
        #TIME
        clock.tick(60)
        screen.fill((0,0,0))
        #EVENT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False    
            elif event.type == pygame.JOYHATMOTION:
                    if event.joy == 0:
                        if event.value == (1,0):
                            player2.change_direction((0, -1))
                        elif event.value == (-1,0):
                            player2.change_direction((0,1))
                                                
                                                    
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player1.change_direction((0, 1))
                elif event.key == pygame.K_RIGHT:
                    player1.change_direction((0, -1))
                elif event.key == pygame.K_a:
                    player2.change_direction((0, 1))
                elif event.key == pygame.K_d:
                    player2.change_direction((0, -1))   
                elif event.key == pygame.K_ESCAPE:
                    keepGoing = False                        
        #changes direction and speeds up ball if ball hits paddle 1           
        if ball.rect.colliderect(player1.rect):
            hit_sound.play()
            ball.change_hit()  
        #changes direction and speeds up ball if ball hits paddle 2
        elif ball.rect.colliderect(player2.rect):   
            hit_sound.play()
            ball.change_hit()                   
        #checks if hits the endzone 
        if ball.rect.colliderect(endzone):
            error_sound.play()
            lives_keeper.lost_life()

            ball.change_direction()
        #checks for points and recongize is two blocks are hit at once 
        points_list = pygame.sprite.spritecollide(ball,blocks_group,False)
        if pygame.sprite.spritecollide(ball,blocks_group,True):
            for points in range(len(points_list)):
                score_keeper.scored_points() 
                blocks_hit_list.append(points_list)
            ball.change_block_hit()
            #Determines when to half the size of the paddle
            if (len(blocks_hit_list) == 60):
                player1.half_paddle() 
                player2.half_paddle()  
        #checks if it hits the white block and adds 50 bonus points and a life
        if pygame.sprite.spritecollide(ball,white_block,True):
            lives_keeper.add_life()
        #Checks if you still have lives left.
        if lives_keeper.get_life() == 0:
            fail_sound.play()
            message = message_font.render("Game Over",1,(255,100,0))
            keepGoing = False
        #Checks if player has won
        if len(blocks_hit_list) == 108:
            winner_sound.play()
            message = message_font.render(" WINNER  ",1,(255,255,255))
            keepGoing = False
         
        #REFRESH
        #blit album art so the ball won't erase it
        screen.blit(wallpaper,(0,0)) 
        screen.blit(album_art,(815,510))
        screen.blit(intro,(75,660))
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)        
        pygame.display.flip()
           
    #Unhide the mouse pointer and display and game over sign
    pygame.mixer.music.fadeout(5000)
    pygame.mouse.set_visible(True)  
    screen.blit(message,(230,300))
    pygame.display.flip()
    pygame.time.wait(5000)
    pygame.quit()
        
main()