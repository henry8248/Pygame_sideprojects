#Import the pygame library and initialize the game engine
import pygame
#import Paddle class from paddle.py
from paddle import Paddle
from ball import Ball
from brick import Brick
pygame.init()

#Define some colors and two global variables
WHITE = (255,255,255)
DARKBLUE = (36,90,190)
LIGHTBLUE = (0,176,240)
RED = (255,0,0)
ORANGE = (255,100,0)
YELLOW = (255,255,0)

score = 0
lives = 3

#Open a new window
size = (800,600) #(width, height)
screen = pygame.display.set_mode((size), pygame.FULLSCREEN)
pygame.display.set_caption("Breakout Game") #window's name

#This will be a list that will contain all the sprites we intend to use in our game.
all_sprites_list = pygame.sprite.Group()

#Create the paddle object
paddle = Paddle(LIGHTBLUE, 100, 10)

#Create the ball sprite
ball = Ball(WHITE,20,20)
ball.rect.x = 345
ball.rect.y = 195

all_bricks = pygame.sprite.Group()
#instantiate bricks
for i in range(7):
    brick = Brick(RED,80,30)
    brick.rect.x = 60 + i*100
    brick.rect.y = 60
    all_sprites_list.add(brick)
    all_bricks.add(brick)
for i in range(7):
    brick = Brick(ORANGE,80,30)
    brick.rect.x = 60 + i* 100
    brick.rect.y = 100
    all_sprites_list.add(brick)
    all_bricks.add(brick)
for i in range(7):
    brick = Brick(YELLOW,80,30)
    brick.rect.x = 60 + i* 100
    brick.rect.y = 140
    all_sprites_list.add(brick)
    all_bricks.add(brick)
#reset paddle position
paddle.rect.x = 350 
paddle.rect.y = 560

all_sprites_list.add(paddle)
all_sprites_list.add(ball)
# The loop will carry on until the user exits the game (e.g. clicks the close button)
carryOn = False
#The clock will be used to control how fast the screen updates
clock = pygame.time.Clock() #create clock object
font = pygame.font.Font(None, 64)
text = font.render("Press enter to start", 1, WHITE)
screen.blit(text, (250,300))
pygame.display.flip()
pygame.time.wait(3000)
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                carryOn = True
               
    if carryOn:
        break
        

#-------Main Programm Loop ----------
while carryOn:
    #----Main event loop
    #1.
    for event in pygame.event.get(): #listens events from user
        if event.type == pygame.QUIT:#if user clicked close
            carryOn = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x: #Pressing the x Key will quit the game
                carryOn = False

    #Moving the paddle when the user uses the arrow keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle.moveLeft(5)

    if keys[pygame.K_RIGHT]:
        paddle.moveRight(5)
    #2. ----Game logic should go here
    all_sprites_list.update()
    #call update method in every sprite classes

    #Check if the ball is bouncing against any of the 4 walls
    if ball.rect.x >= 790:
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.x <= 0:
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.y > 590:
        lives -= 1
        if lives == 0:
            #display game over message for 3 seconds
            text2.fill(DARKBLUE) #erase old text on the surface
            screen.blit(text2,(650,10))
            text2 = font.render("Lives: " + str(lives), 1, WHITE)
            #create a new surface with text on it
            screen.blit(text2, (650,10))
            font = pygame.font.Font(None, 74)
            text = font.render("GAME OVER", 1, WHITE)
            screen.blit(text, (250,300))
            pygame.display.flip()
            pygame.time.wait(3000)
            carryOn = False
        else:
            ball.rect.x = 250
            ball.rect.y = 300
            ball.revelocity()
    if ball.rect.y < 40:
        ball.velocity[1] = -ball.velocity[1]
        #Detect collisions between the ball and the paddles
    if pygame.sprite.collide_mask(ball, paddle):
        #ball.rect.x -= ball.velocity[0]
        #ball.rect.y -= ball.velocity[1]
        ball.bounce()
        #Check if there is the ball collides with any of bricks
    brick_collision_list = pygame.sprite.spritecollide(ball,all_bricks, True)
    for brick in brick_collision_list:
        ball.bounce()
        score += 1
        brick.kill()
        if len(all_bricks) == 0:
        #Display Level Complete Message for 3 seconds
            screen.fill(DARKBLUE)
            pygame.draw.line(screen, WHITE, [0, 38], [800, 38], 2) #width = 2

            #draw all the sprites in one go.
            all_sprites_list.draw(screen)
            text1.fill(DARKBLUE) #erase old text on the surface
            screen.blit(text1,(20,10))
            text1 = font.render("Score: " + str(score), 1, WHITE)
            #create a new surface with text on it
            screen.blit(text1, (20,10))
            font = pygame.font.Font(None, 74)
            text = font.render("LEVEL COMPLETE", 1, WHITE)
            screen.blit(text, (200,300))
            pygame.display.flip()
            pygame.time.wait(3000)
                     
            #Stop the Game
            carryOn = False
    # --- Drawing code should go here
    # First, clear the screen to dark blue
    screen.fill(DARKBLUE) #1
    pygame.draw.line(screen, WHITE, [0, 38], [800, 38], 2) #width = 2 #2

    #draw all the sprites in one go.
    all_sprites_list.draw(screen) #3
    #1.2.3-> update the screen
    #Display the score and the number of lives at the top of the screen
    font = pygame.font.Font(None, 34)
    text1 = font.render("Score: " + str(score), 1, WHITE)
    screen.blit(text1, (20,10))
    text2 = font.render("Lives: " + str(lives), 1, WHITE)
    screen.blit(text2, (650,10))

    #--- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    # --- Limit to 60 frames per second
    clock.tick(60)
pygame.quit() #stop the game engine
