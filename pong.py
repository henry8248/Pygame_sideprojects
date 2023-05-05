import pygame
import random as r
pygame.init()
BLACK = (0,0,0)
WHITE = (255,255,255)
scoreL = 0
scoreR = 0
size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pong")
all_sprites_list = pygame.sprite.Group()

class Paddle(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.rect(self.image, color, [0,0,width, height])
        self.rect = self.image.get_rect()
    def moveUp(self, pixels):
        self.rect.y -= pixels
        if self.rect.y <= 55:
            self.rect.y = 55
    def moveDown(self, pixels):
        self.rect.y += pixels
        if self.rect.y >= 500:
            self.rect.y = 500
class Ball(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.circle(self.image, color, [width//2, height//2],10)
        self.rect = self.image.get_rect()
        v_x = 0
        self.velocity = [0,0]
        select = r.randint(1,2)
        while not v_x:
            if select == 1:
                v_x = r.randint(-4,-2)
            else:
                v_x = r.randint(2, 4)
        else:
            self.velocity = [v_x, r.randint(-4,4)]
    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
    def bounce(self):
        self.velocity[0] = -self.velocity[0]
    def bouncebywall(self):
        self.velocity[1] = -self.velocity[1]
    def reset_vel(self):
        v_x = 0
        select = r.randint(1,2)
        while not v_x:
            if select == 1:
                v_x = r.randint(-4,-2)
            else:
                v_x = r.randint(2, 4)
        else:
            self.velocity = [v_x, r.randint(-4,4)]
paddle1 = Paddle(WHITE, 10, 100)
paddle2 = Paddle(WHITE, 10, 100)
paddle1.rect.x = 50
paddle1.rect.y = 250
paddle2.rect.x = 740
paddle2.rect.y = 250
ball = Ball(WHITE, 20, 20)
ball.rect.x = 390
ball.rect.y = 290
all_sprites_list.add(paddle1)
all_sprites_list.add(paddle2)
all_sprites_list.add(ball)
carryOn = False
clock = pygame.time.Clock()
font = pygame.font.Font(None, 64)
text = font.render("Press enter to start", 1, WHITE)
screen.blit(text, (250,300))
pygame.display.flip()
pygame.time.wait(3000)
while not carryOn:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                carryOn = True


while carryOn:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            carryOn = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        paddle2.moveUp(5)
    if keys[pygame.K_DOWN]:
        paddle2.moveDown(5)
    if keys[pygame.K_w]:
        paddle1.moveUp(5)
    if keys[pygame.K_s]:
        paddle1.moveDown(5)
    all_sprites_list.update()
    
    if ball.rect.y <= 55 or ball.rect.y >= 580:
        ball.bouncebywall()
    elif ball.rect.x <= 0:
        scoreR += 1
        ball.reset_vel()
        ball.rect.x = 390
        ball.rect.y = 290
    elif ball.rect.x >= 780:
        scoreL += 1
        ball.reset_vel()
        ball.rect.x = 390
        ball.rect.y = 290
    #    ball.bounce()
    if scoreL == 10 or scoreR == 10:
        if scoreL == 10:
            textL.fill(BLACK)
            screen.blit(textL, (10,10))
            textL = font.render(str(scoreL),1,WHITE)
            screen.blit(textL, (10,10))
        elif scoreR == 10:
            textR.fill(BLACK)
            screen.blit(textR, (10,10))
            textR = font.render(str(scoreR),1,WHITE)
            screen.blit(textR, (10,10))
        font = pygame.font.Font(None, 74)
        text = font.render("Someone wins!",1,WHITE)
        screen.blit(text, (200, 250))
        pygame.display.flip()
        pygame.time.wait(3000)
        break
    #draw and refresh the screen
    if pygame.sprite.collide_mask(ball, paddle1):
        ball.bounce()
    elif pygame.sprite.collide_mask(ball, paddle2):
        ball.bounce()
    screen.fill(BLACK)
    pygame.draw.line(screen, WHITE, [0,50], [800,50], 5)
    pygame.draw.line(screen, WHITE, [400,0], [400,800],5)
    all_sprites_list.draw(screen)
    font = pygame.font.Font(None, 34)
    textL = font.render(str(scoreL),1,WHITE)
    screen.blit(textL, (10,10))
    font = pygame.font.Font(None, 34)
    textR = font.render(str(scoreR),1,WHITE)
    screen.blit(textR, (770,10))
    
    pygame.display.flip()
    clock.tick(60)

    
pygame.quit()
    
