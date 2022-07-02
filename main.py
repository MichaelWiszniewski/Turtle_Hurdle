"""
-------------------------------------------------------------------------------
Name:   main.py
Purpose:  This program runs a game called "Turtle Hurdle", where two turtles
(Tim and Terrence) exchange fire while dodging hurdles and the objective is to 
keep as many lives as possible.
 
Authors: Michael Wiszniewski, Andreas Nikitopolous, Lucas Marques,
Matthew Melo
 
Created:  date in 12/06/2022
------------------------------------------------------------------------------
"""

'''
The first thing to do was import the libraries and modules which are 
going to be needed to create this game in order to call various 
functions
'''
from logging.handlers import WatchedFileHandler
from operator import truediv
from pickle import FALSE
from re import M
import pygame
import os
from pygame import mixer
import random

#These commands initialize all imported modules in order for them to be used
pygame.init()
pygame.font.init()
pygame.mixer.init()

#Set the parameters for the window
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Turtle Hurdle!")

#define colours needed
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GRAY=(50, 50, 50)
GREEN=(0, 255, 0)
BLUE=(0, 0, 255)

#This is the green border seen in between the two sides
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

#These are the sound effects heard throughout the game
BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Got_hit_sound.wav')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/Shooting_sound.wav')
HURDLE_HIT_SOUND = pygame.mixer.Sound('Assets/Short_explosion.wav')

#This is the background Music
mixer.music.load('Assets/Background2.mp3')
mixer.music.play(10)

#Setting each font used on the screen
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 75)
MENU_FONT = pygame.font.SysFont('comicsans', 50)
HOW_TO_PLAY_FONT = pygame.font.SysFont('comicsans', 35)
HOW_TO_FONT = pygame.font.SysFont("comicsans", 25)


#Set the frames per second this game will run at
FPS = 30

#Velocity of charachter movement
VEL = 5

#Velocity of bullet movement
BULLET_VEL = 16

#Amount of bullets that can be shot without delay
MAX_BULLETS = 2

#The max amount of hurdles on the screen at a time
MAX_HURDLES = 1

#Velocity of moving hurdles in level 2
HURDLE_VEL = 12

#Size of both Tim and Terrence turtles
TURTLE_WIDTH, TURTLE_HEIGHT = 55, 40

#Setting each event which requires conditionals
TIM_HIT = pygame.USEREVENT + 1
TERRENCE_HIT = pygame.USEREVENT + 2
TIM_HIT_BY_HURDLE = pygame.USEREVENT + 3
TERRENCE_HIT_BY_HURDLE = pygame.USEREVENT + 4
#Events to trigger hurdle creation
TERRENCE_HURDLE_SPAWN = pygame.USEREVENT + 5
TIM_HURDLE_SPAWN = pygame.USEREVENT + 6

#This variable is loading the image of Tim the turtle into pygame
TIM_TURTLE_IMAGE = pygame.image.load(
    os.path.join('Assets', 'tim_turtle.png'))

#This variable is putting tim the turtle on to the screen with the correct dimentions and orientation
TIM_TURTLE = pygame.transform.rotate(pygame.transform.scale(
    TIM_TURTLE_IMAGE, (TURTLE_WIDTH, TURTLE_HEIGHT)), 0)

#This variable is loading the image of Terrence the turtle into pygame
TERRENCE_TURTLE_IMAGE = pygame.image.load(
    os.path.join('Assets', 'terrence_turtle.png'))

#This variable is putting terrence the turtle on to the screen with the correct dimentions and orientation
TERRENCE_TURTLE = pygame.transform.rotate(pygame.transform.scale(
    TERRENCE_TURTLE_IMAGE, (TURTLE_WIDTH, TURTLE_HEIGHT)), 0)

#This variable contains the background scenery seen in the first level
SCENERY = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'forest.png')), (WIDTH, HEIGHT))

#This variable contains the background scenery seen in the second level
SCENERYV2 = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'level_2_background.png')), (WIDTH, HEIGHT))


#This variable contains the image of the hurdle seen throughout the game
HURDLE_IMAGE = pygame.image.load(
    os.path.join('Assets', 'hurdle.png'))

#This variable is orienting and inserting the hurdle images on to the screen
HURDLE=pygame.transform.rotate(pygame.transform.scale(
    HURDLE_IMAGE, (60, 60)), 0)


#track game state (levels), this was used for bug troubleshooting
gameState=0

# MENU Text Renderer
def text_format(message, textFont, textSize, textColor):
    newText = MENU_FONT.render(message, textSize, textColor)
    return newText

# instructions text Renderer
def text1_format(message, textFont, textSize, textColor):
    new1Text = HOW_TO_FONT.render(message, textSize, textColor)
    return new1Text

# How to play title text Renderer
def text2_format(message, textFont, textSize, textColor):
    new1Text = HOW_TO_PLAY_FONT.render(message, textSize, textColor)
    return new1Text

#Insert function for level 1 drawing game window 
def draw_window(terrence, tim, terrence_bullets, tim_bullets, terrence_health, tim_health, scenery):
    WIN.blit(scenery, (0, 0))
    pygame.draw.rect(WIN, GREEN, BORDER)

    #These variables contain the health counters seen throughout level 1
    terrence_health_text = HEALTH_FONT.render(
        "Terrence Health: " + str(terrence_health), 1, BLACK)
    tim_health_text = HEALTH_FONT.render(
        "Tim Health: " + str(tim_health), 1, BLACK)
    
    #Inserting level 1 health counters on to the screen
    WIN.blit(terrence_health_text, (WIDTH - terrence_health_text.get_width() - 10, 10))
    WIN.blit(tim_health_text, (10, 10))

    #Inserting Tim and Terrence on to the screen for level 1
    WIN.blit(TIM_TURTLE, (tim.x, tim.y))
    WIN.blit(TERRENCE_TURTLE, (terrence.x, terrence.y))

    #Drawing Tim and Terrences bullets on to the screen for level 1
    for bullet in terrence_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in tim_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    #Updating the display so that each visual in level 1 is viewable from pygame commands
    pygame.display.update()

#Insert function for level 2 drawing game window
def draw_window2(terrence, tim, terrence_bullets, tim_bullets, terrence_health, tim_health, scenery, terrence_hurdles, tim_hurdles):
    WIN.blit(scenery, (0, 0))
    pygame.draw.rect(WIN, GREEN, BORDER)

    #These variables contain the health counters seen throughout level 2
    terrence_health_text = HEALTH_FONT.render(
        "Terrence Health: " + str(terrence_health), 1, WHITE)
    tim_health_text = HEALTH_FONT.render(
        "Tim Health: " + str(tim_health), 1, WHITE)
    
    #Inserting level 2 health counters on to the screen
    WIN.blit(terrence_health_text, (WIDTH - terrence_health_text.get_width() - 10, 10))
    WIN.blit(tim_health_text, (10, 10))

    #Inserting Tim and Terrence on to the screen for level 2
    WIN.blit(TIM_TURTLE, (tim.x, tim.y))
    WIN.blit(TERRENCE_TURTLE, (terrence.x, terrence.y))

    #Drawing Tim and Terrences bullets and hurdles on to the screen for level 2
    for bullet in terrence_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in tim_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    for hurdle in terrence_hurdles:
        WIN.blit(HURDLE, (hurdle.x,hurdle.y))

    for hurdle in tim_hurdles:
        WIN.blit(HURDLE, (hurdle.x,hurdle.y))

    #Updating the display so that each visual in level 2 is viewable from pygame commands
    pygame.display.update()

'''
This is the function which contains all of the movement logic and 
user interactions for Tim and "off the screen" logic
'''
def tim_handle_movement(keys_pressed, tim):
    if keys_pressed[pygame.K_a] and tim.x - VEL > 0:  # LEFT
        tim.x -= VEL
    if keys_pressed[pygame.K_d] and tim.x + VEL + tim.width < BORDER.x:  # RIGHT
        tim.x += VEL
    if keys_pressed[pygame.K_w] and tim.y - VEL > 0:  # UP
        tim.y -= VEL
    if keys_pressed[pygame.K_s] and tim.y + VEL + tim.height < HEIGHT - 15:  # DOWN
        tim.y += VEL
'''
This is the function which contains all of the movement logic and 
user interactions for Terrence and "off the screen" logic
'''
def terrence_handle_movement(keys_pressed, terrence):
    if keys_pressed[pygame.K_LEFT] and terrence.x - VEL > BORDER.x + BORDER.width:  # LEFT
        terrence.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and terrence.x + VEL + terrence.width < WIDTH:  # RIGHT
        terrence.x += VEL
    if keys_pressed[pygame.K_UP] and terrence.y - VEL > 0:  # UP
        terrence.y -= VEL
    if keys_pressed[pygame.K_DOWN] and terrence.y + VEL + terrence.height < HEIGHT - 15:  # DOWN
        terrence.y += VEL

#Define the bullets collision, movement, or "off the screen" logic
def handle_bullets(tim_bullets, terrence_bullets, tim, terrence):
    for bullet in tim_bullets:
        bullet.x += BULLET_VEL
        if terrence.colliderect(bullet):
            pygame.event.post(pygame.event.Event(TERRENCE_HIT))
            tim_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            tim_bullets.remove(bullet)

    for bullet in terrence_bullets:
        bullet.x -= BULLET_VEL
        if tim.colliderect(bullet):
            pygame.event.post(pygame.event.Event(TIM_HIT))
            terrence_bullets.remove(bullet)
        elif bullet.x < 0:
            terrence_bullets.remove(bullet)

#Define the hurdle obstacles position or "off the screen" logic
def handle_hurdle(tim_hurdles, terrence_hurdles, tim, terrence):
    for hurdle in tim_hurdles:
        hurdle.x += HURDLE_VEL
        if terrence.colliderect(hurdle):
            pygame.event.post(pygame.event.Event(TERRENCE_HIT_BY_HURDLE))
            tim_hurdles.remove(hurdle)
        elif hurdle.x > WIDTH:
            tim_hurdles.remove(hurdle)

    for hurdle in terrence_hurdles:
        hurdle.x -= HURDLE_VEL
        if tim.colliderect(hurdle):
            pygame.event.post(pygame.event.Event(TIM_HIT_BY_HURDLE))
            terrence_hurdles.remove(hurdle)
        elif hurdle.x < 0:
            terrence_hurdles.remove(hurdle)

#This function declares and calls the text which states the winner after each round
def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, RED)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    
    #Updating the display so that each visual viewable from pygame commands
    pygame.display.update()
    
    #This line causes the pause to view the winning text
    pygame.time.delay(5000)

'''
This is the main game function, 
where every function is called, 
and every game loop occurs, 
combining to make the game
'''
def main():
    
    #Drawing a rectangle for Terrence and Tim (helps with all around game logic)
    terrence = pygame.Rect(700, 300, TURTLE_WIDTH, TURTLE_HEIGHT)
    tim = pygame.Rect(100, 300, TURTLE_WIDTH, TURTLE_HEIGHT)

    #This function is used to create a clock object which is used to keep track of time
    clock = pygame.time.Clock()

    #Initialize Level 1 lives/bullet capacity
    terrence_bullets = []
    tim_bullets = []
    terrence_health = 5
    tim_health = 5
    
    #Initialize main menu screen seen before level 1
    menu=True
    
    #Create empty string which will be used for main menu logic
    selected=""
    
    #This was used for bug troubleshooting
    print("Starting Menu Menu Screen")
    
    #This is the main menu loop
    while menu:
        
        #Uses time measurement to track frames/second
        clock.tick(FPS)
        
        #Catch main menu keyboard events 
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            
            #Catch when user presses a key
            if event.type==pygame.KEYDOWN:
                
                #Catch when user presses up arrow to highlight start
                if event.key==pygame.K_UP:
                    selected="start"
                
                #Catch when user presses down arrow to highlight quit
                elif event.key==pygame.K_DOWN:
                    selected="quit"
                
                #Catches when user presses return to start the game
                if event.key==pygame.K_RETURN:
                    if selected=="start":
                        print("Start")
                        
                        #This breaks out of menu loop and into level 1 loop
                        menu=False
                        
                        #This was used for bug troubleshooting to mesure when main menu ends
                        print("Exiting main menu screen ") 
                    
                    #This closes the window if user presses quit
                    if selected=="quit":
                        pygame.quit()
                        quit()
        
        # draw and update Main Menu UI
        WIN.fill(BLACK)
        
        #This variable holds the title text in main menu
        title=text_format("TURTLE HURDLE!", MENU_FONT, 90, GREEN)
        
        #This variable holds the how to play sign text
        how_to_play = text2_format("HOW TO PLAY: ", HOW_TO_PLAY_FONT, 75, WHITE)
        
        #This variable holds Tims user instructions and controls
        tim_instructions = text1_format("LEFT PLAYER (TIM) movement: a w s d keys, shooting: left shift", HOW_TO_FONT, 75, WHITE)
        
        #This variable holds Terrences user instructions and controls
        terrence_instructions = text1_format("RIGHT PLAYER (TERRENCE) movement: arrow keys, shooting: right alt", HOW_TO_FONT, 75, WHITE)
        
        #This variable holds the first line of the aim of game
        aim_of_game1 = text1_format("Dodge other players bullets and hurdles and shoot other player!", HOW_TO_FONT, 75, WHITE)
        
        #This variable holds the second line of the aim of game
        aim_of_game2 = text1_format("Remaining lives from each round determine each players points!", HOW_TO_FONT, 75, WHITE)
        
        #These hold the conditions and outcomes of each selection in the main menu
        if selected=="start":
            text_start=text_format("START", MENU_FONT, 75, GREEN)
        else:
            text_start = text_format("START", MENU_FONT, 75, WHITE)
        if selected=="quit":
            text_quit=text_format("QUIT", MENU_FONT, 75, GREEN)
        else:
            text_quit = text_format("QUIT", MENU_FONT, 75, WHITE)
 
        '''
        Below, every variable declared for the main menu is given a rectangle 
        which makes it possible to insert them on to the screen
        '''
        title_rect=title.get_rect()
        start_rect=text_start.get_rect()
        quit_rect=text_quit.get_rect()
        how_to_play_rect=how_to_play.get_rect()
        tim_instructions_rect=tim_instructions.get_rect()
        terrence_instructions_rect=terrence_instructions.get_rect()
        aim_of_game1_rect=aim_of_game1.get_rect()
        aim_of_game2_rect=aim_of_game2.get_rect()
 
        # Main Menu Text positioning
        WIN.blit(title, (WIDTH/2 - (title_rect[2]/2), 20))
        WIN.blit(text_start, (WIDTH/2 - (start_rect[2]/2), 100))
        WIN.blit(text_quit, (WIDTH/2 - (quit_rect[2]/2), 150))
        WIN.blit(how_to_play, (WIDTH/2 - (how_to_play_rect[2]/2), 240))
        WIN.blit(tim_instructions, (WIDTH/2 - (tim_instructions_rect[2]/2), 310))
        WIN.blit(terrence_instructions, (WIDTH/2 - (terrence_instructions_rect[2]/2), 360))
        WIN.blit(aim_of_game1, (WIDTH/2 - (aim_of_game1_rect[2]/2), 410))
        WIN.blit(aim_of_game2, (WIDTH/2 - (aim_of_game2_rect[2]/2), 460))
        
        #Updating the display so that each visual viewable from pygame commands
        pygame.display.update()
        
        #Setting the caption of the window to an appropriate name
        pygame.display.set_caption("Turtle Hurdle!")
    #end of main menu    

    #Tracking game level which helped with debugging
    gameState=1 
    
    #Setting condition which initializes the while loop
    run = True
    
    #Printing game level which helped with debugging
    print(gameState)
    print("Starting Level 1")

    #Level 1 loop
    while run:    
        
        #Uses time measurement to track frames/second
        clock.tick(FPS)
        
        #catch main menu keyboard events 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            #Catch when user presses a key
            if event.type == pygame.KEYDOWN:
                
                #Catch when Tim user presses key to shoot and make sure they can only shoot 2 at a time
                if event.key == pygame.K_LSHIFT and len(tim_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        tim.x + tim.width, tim.y + tim.height//2 - 2, 10, 5)
                    tim_bullets.append(bullet)
                    
                    #Plays bullet shot sound effect
                    BULLET_FIRE_SOUND.play()

                #Catch when Terrence user presses key to shoot and make sure they can only shoot 2 at a time
                if event.key == pygame.K_RALT and len(terrence_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        terrence.x, terrence.y + terrence.height//2 - 2, 10, 5)
                    terrence_bullets.append(bullet)
                    
                    #Plays bullet shot sound effect
                    BULLET_FIRE_SOUND.play()

            #Subtracting one from Terrence health when hit by bullet
            if event.type == TERRENCE_HIT:
                terrence_health -= 1
                
                #Plays hit by bullet sound effect
                BULLET_HIT_SOUND.play()

            #Subtracting one from Tim health when hit by bullet
            if event.type == TIM_HIT:
                tim_health -= 1
                
                #Plays hit by bullet sound effect
                BULLET_HIT_SOUND.play()

        #Create the empty string variables which displays the winner of level 1 and their points in that level
        winner_text = ""
        
        #Condition required for tim to win level 1
        if terrence_health <= 0:
            winner_text = "Tim Wins Level 1!"

        #Condition required for terrence to win level 1
        if tim_health <= 0:
            winner_text = "Terrence Wins Level 1!"

        #This if statement lets the program know when to stop running level 1 based on if there is a winner yet
        if winner_text != "":
            draw_winner(winner_text)
            #break
            run=False
            
            #Prints statement when exiting first level to help with debugging
            print("Exiting Level 1")

        
        #Below, every variable declared for level 1 is called 
        keys_pressed = pygame.key.get_pressed()
        tim_handle_movement(keys_pressed, tim)
        terrence_handle_movement(keys_pressed, terrence)

        handle_bullets(tim_bullets, terrence_bullets, tim, terrence)

        draw_window(terrence, tim, terrence_bullets, tim_bullets,
                    terrence_health, tim_health, SCENERY)
    
    #Calculate each players points earned in round 1 
    tim_round1_points = tim_health*3
    terrence_round1_points = terrence_health*3

    #Transition from level 1 to level 2
    #Reuse code from main menu
    #initialize transitional menu screen 
    menu=True
    selected=""
    print("Starting transitional Menu Screen")
    while menu:
        clock.tick(FPS)
        #catch transitional menu keyboard events 
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP:
                    selected="continue"
                elif event.key==pygame.K_DOWN:
                    selected="quit"
                if event.key==pygame.K_RETURN:
                    if selected=="continue":
                        print("Start")
                        menu=False
                        print("Exiting transitional menu screen ") #exit while loop
        
        
        #draw and update transitional Menu UI
        WIN.fill(BLACK)
        title=text_format("On to level 2!", MENU_FONT, 90, GREEN)
        tim_mid_score = text_format("Tim round 1 points: " + str(tim_round1_points), MENU_FONT, 90, WHITE)
        terrence_mid_score = text_format("Terrence round 1 points: " + str(terrence_round1_points), MENU_FONT, 90, WHITE)
        if selected=="continue":
            text_start=text_format("CONTINUE", MENU_FONT, 75, GREEN)
        else:
            text_start = text_format("CONTINUE", MENU_FONT, 75, WHITE)
 
        title_rect=title.get_rect()
        start_rect=text_start.get_rect()

        #Creating the rectangles which allow me to use blit function
        tim_mid_score_rect = tim_mid_score.get_rect()
        terrence_mid_score_rect = terrence_mid_score.get_rect()
 
        #Using the blit function to display the game result text on the screen 
        WIN.blit(title, (WIDTH/2 - (title_rect[2]/2), 80))
        WIN.blit(text_start, (WIDTH/2 - (start_rect[2]/2), 200))
        WIN.blit(tim_mid_score, (WIDTH/2 - (tim_mid_score_rect[2]/2), 300))
        WIN.blit(terrence_mid_score, (WIDTH/2 - (terrence_mid_score_rect[2]/2), 360))
        WIN.blit(TIM_TURTLE, (120, 320))
        WIN.blit(TERRENCE_TURTLE, (50, 380))
        
        #Updating the display so that each visual viewable from pygame commands
        pygame.display.update()
        
        pygame.display.set_caption("Turtle Hurdle!")
    #end of transitional menu

    #Check if calculator is functioning
    print("Tim 1st round pts: " + str(tim_round1_points))
    print("Terrence 1st round pts: " + str(terrence_round1_points))

    #initialize (reset) Level 2 values and variables
    gameState=2
    run = True
    print(gameState)
    print("Start Level 2 Here")
    terrence_bullets = []
    tim_bullets = []
    terrence_health = 10
    tim_health = 10      
    
    #Declare empty list variables to hold hurdles on the screen
    tim_hurdles = []
    terrence_hurdles = []

    #Level 2 loop
    while run:    
        
        #Uses time measurement to track frames/second
        clock.tick(FPS)
        
        #Catch main menu keyboard events 
        for event in pygame.event.get():
            
            #Lets program know when to quit
            if event.type == pygame.QUIT:
                pygame.quit()

            #These are the possible scenarios and outcomes when a key on the keyboard is pressed by the user
            if event.type == pygame.KEYDOWN:
                
                #These are the conditions required for tim to shoot a bullet
                if event.key == pygame.K_LSHIFT and len(tim_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        tim.x + tim.width, tim.y + tim.height//2 - 2, 10, 5)
                    tim_bullets.append(bullet)
                    
                    #Plays bullet firing sound
                    BULLET_FIRE_SOUND.play()

                #These are the conditions required for terrence to shoot a bullet
                if event.key == pygame.K_RALT and len(terrence_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        terrence.x, terrence.y + terrence.height//2 - 2, 10, 5)
                    terrence_bullets.append(bullet)
                    
                    #Plays bullet firing sound
                    BULLET_FIRE_SOUND.play()

            #Occurances when terrence is hit by a bullet
            if event.type == TERRENCE_HIT:
                terrence_health -= 1
                BULLET_HIT_SOUND.play()

            #Occurances when tim is hit by a bullet
            if event.type == TIM_HIT:
                tim_health -= 1
                BULLET_HIT_SOUND.play()

            #Occurances when terrence is hit by a hurdle
            if event.type == TERRENCE_HIT_BY_HURDLE:
                terrence_health -= 1
                HURDLE_HIT_SOUND.play()

            #Occurances when tim is hit by a hurdle
            if event.type == TIM_HIT_BY_HURDLE:
                tim_health -= 1
                HURDLE_HIT_SOUND.play()
        
        #Create the empty string variables which displays the winner of level 2 and their points in that level
        winner_text = ""
        
        #Condition required for tim to win level 2
        if terrence_health <= 0:
            winner_text = "Tim Wins Level 2!"

        #Condition required for terrence to win level 2
        if tim_health <= 0:
            winner_text = "Terrence Wins Level 2!"

        #This if statement lets the program know when to stop running level 2
        if winner_text != "":
            draw_winner(winner_text)
            #break
            run=False
            print("Exiting Level 2")

        #Check if you need to spawn a hurdle on terrence side
        if len(terrence_hurdles) < MAX_HURDLES:
            hurdle = pygame.Rect(WIDTH - 60, random.randint(0, HEIGHT), 60, 60)
            terrence_hurdles.append(hurdle)

        #Check if you need to spawn a hurdle on tim side
        if len(tim_hurdles) < MAX_HURDLES:
            hurdle = pygame.Rect(0, random.randint(0, HEIGHT), 60, 60)
            tim_hurdles.append(hurdle)

        '''
        Below, all of the functions previously written are 
        being called into the main game loop for level 2
        '''
        keys_pressed = pygame.key.get_pressed()
        tim_handle_movement(keys_pressed, tim)
        terrence_handle_movement(keys_pressed, terrence)

        handle_bullets(tim_bullets, terrence_bullets, tim, terrence)

        handle_hurdle(tim_hurdles, terrence_hurdles, tim, terrence)

        draw_window2(terrence, tim, terrence_bullets, tim_bullets,
                    terrence_health, tim_health, SCENERYV2, terrence_hurdles, tim_hurdles)
    
    #Calculate each players points earned in round 2
    tim_round2_points = tim_health *3
    terrence_round2_points = terrence_health *3

    #Check if calculator is functioning
    print("Tim 2nd round pts: " + str(tim_round2_points))
    print("Terrence 2nd round pts: " + str(terrence_round2_points))


    #Calculate each players points earned in total
    tim_total_points = tim_round1_points + tim_round2_points
    terrence_total_points = terrence_round1_points + terrence_round2_points

    #Insert Last slide displaying winner
    menu=True
    print("Starting end results Screen")
    while menu:
        
        #Uses time measurement to track frames/second
        clock.tick(FPS)
        
        #catch transitional menu keyboard events 
        for event in pygame.event.get():
            
            #Lets program know when to quit
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
        
        
        #draw and update transitional Menu UI
        WIN.fill(BLACK)
        
        #The 3 possible scenarios of the game and their messages
        if terrence_total_points > tim_total_points:
            victor = "Terrence wins the game!"

        elif tim_total_points > terrence_total_points:
            victor = "Tim wins the game!"

        elif tim_total_points == terrence_total_points:
            victor = "It is a tie!"

        #Setting the variables containing each players total score counter for the end of the game
        end_result = text_format(victor, MENU_FONT, 90, GREEN)
        tim_score = text_format("Tim total points: " + str(tim_total_points), MENU_FONT, 90, WHITE)
        terrence_score = text_format("Terrence total points: " + str(terrence_total_points), MENU_FONT, 90, WHITE)

        #Creating the rectangles for each score which allow to use blit function to put the scores on final menu screen
        end_result_rect = end_result.get_rect()
        tim_score_rect = tim_score.get_rect()
        terrence_score_rect = terrence_score.get_rect()
 
        #Using the blit function to display the game result text on the screen 
        WIN.blit(end_result, (WIDTH/2 - (end_result_rect[2]/2), 80))
        
        #Putting the winning turtle on the final screen next to winning text
        if terrence_total_points > tim_total_points:
            WIN.blit(TERRENCE_TURTLE, (80, 100))
        elif tim_total_points > terrence_total_points:
            WIN.blit(TIM_TURTLE, (80, 100))
        
        #Putting Tims score on the final screen 
        WIN.blit(tim_score, (WIDTH/2 - (tim_score_rect[2]/2), 250))
        
        #Putting Terrences score on the final screen
        WIN.blit(terrence_score, (WIDTH/2 - (terrence_score_rect[2]/2), 360))
        
        #Putting Tim image next to Tims final score
        WIN.blit(TIM_TURTLE, (110, 270))
        
        #Putting Terrence image next to Terrences final score
        WIN.blit(TERRENCE_TURTLE, (50, 380))
        
        #Updating the display so that each visual viewable from pygame commands
        pygame.display.update()
        
        pygame.display.set_caption("Turtle Hurdle!")
    #end of transitional menu

    #Check if calculator is functioning
    print("Tim total pts: " + str(tim_total_points))
    print("Terrence total pts: " + str(terrence_total_points))

#Calling the main loop which causes the game to run   
main()