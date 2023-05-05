import pygame
# from pygame.locals import
import random
pygame.init()

clock = pygame.time.Clock()
fps = 60 #framrate = 60
screen_width = 864
screen_height = 936

screen = pygame.display.set_mode((screen_width, screen_height))  # create game window
pygame.display.set_caption('Flappy Bird')

#define font
font = pygame.font.SysFont('Bauhaus 93',60) #(font, font.size)

#define colors
white = (255, 255, 255)
#define game variables
ground_scroll = 0
scroll_speed = 4 # 4 pixels
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 1500 #pipe appearing frequency (milliseconds)
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False
#load images
bg = pygame.image.load('bg.png') #default: search file in current directory
ground_img = pygame.image.load("ground.png")
button_img = pygame.image.load('restart.png')
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col) #textcolor
    screen.blit(img, (x, y))

def reset_game():
    pipe_group.empty() #clear pipe_group
    
    flappy.rect.x = 100#reset bird's pos
    flappy.rect.y =int(screen_height / 2)
    score = 0
    
    return score
#to use absolute path, add path in front of filenames
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0 # control the speed of animation runs
        for num in range(1,4): #load images
            img = pygame.image.load(f'bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index] 
        self.rect = self.image.get_rect()
        #Get a rectangle with the size of the image 
        self.rect.center = [x,y]
        self.vel = 0
        self.clicked = False
    def update(self):
        global flying
        if flying: #after the first click will the gravity work(control by 'flying')
            #gravity effect
            
            self.vel += 0.5
            if self.vel > 8: #limit gravity effect
                self.vel = 8
            if self.rect.bottom < 768: #< 768 才更新y.位置
                self.rect.y += int(self.vel)
        else:
            self.vel = 0
           
           
            
           
        #jump
        if game_over == False:

            
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                #when left key of the mouse
                #is pressed
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0: #add this condition logic
                                                   #to reset self.clicked
                self.clicked = False
                
                
            #handle the animation
            
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown: #flip the bird image after iterating
                                             # 5 times
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
                    
            self.image = self.images[self.index] #開始拍翅
            #rotate the bird: face up when flapping upward down when dropping
            self.image = pygame.transform.rotate(self.images[self.index], -2*self.vel) # last param is the angle of rotation
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90) #minus 90 degree



class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('pipe.png')
        self.rect = self.image.get_rect()
        #position 1 is from the top, -1 is from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]
    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
        #畫面捲動出視野即清空pipe_group 避免pipe_group越來越滿，占用game memory
            self.kill()
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    def draw(self):
        action = False
        #get mouse position: is it on top of buttom image?
        pos = pygame.mouse.get_pos()
        #check if mouse is over the button
        if self.rect.collidepoint(pos): #if (x, y) in rect -> True
            if pygame.mouse.get_pressed()[0] == 1: #check click
                action = True
                
                
        #draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action
        
bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()
flappy = Bird(100, int(screen_height / 2))
bird_group.add(flappy)
#create restart button instance
button = Button(screen_width // 2 - 50, screen_height//2 - 100, button_img)

run = True

while run:
 
    
    clock.tick(fps)
    #draw background
    screen.blit(bg, (0,0)) #put bg at (0,0)

    bird_group.draw(screen) 
    bird_group.update()
    pipe_group.draw(screen)

    #check the score
    if len(pipe_group) > 0: #if there are pipes
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and pass_pipe == False: # if the bird is in scoring zone
            pass_pipe = True
        if pass_pipe:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False
    draw_text(str(score), font, white, int(screen_width / 2),20)    
        
        
    #screen.blit(ground_img, (ground_scroll,768)) #put here to stop scroll when touching the ground
    #check if bird has hit the ground
    if flappy.rect.bottom >= 768:
        game_over = True
        flying = False #關掉重力場
        flappy.update()
    if game_over == False and flying == True: #after mouse clicked, pipes pop up
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe >= pipe_frequency: #create new pipes
            pipe_height = random.randint(-100,100)
        
            btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height  ,-1)
            top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height  , 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now
            
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35: #ground sprite is longer than bg sprite by 35 pixels
                                #reset bg and ground position
            ground_scroll = 0
        pipe_group.update() #pipe moves only when ground moves
    screen.blit(ground_img, (ground_scroll,768)) #put here to stop scroll when touching the gr
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True
        

    #check for game over and reset
    if game_over:
        if button.draw():
            game_over = False
            score = reset_game()
            #print(flappy.vel)
            
            #reset game
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False: # if mouse got click and flying = False
            flying = True
        
        
    pygame.display.update() #update the screen
pygame.quit()
