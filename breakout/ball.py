import pygame
from random import randint
BLACK = (0,0,0)

class Ball(pygame.sprite.Sprite):

    def __init__(self, color, width, height):
        super().__init__()
        # Pass in the color of the ball, its width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        
        # Draw the ball (a rectangle!)
        # init position (0,0)
        #pygame.draw.rect(self.image, color, [0, 0, width, height])
        pygame.draw.circle(self.image, color, (width//2,height//2), 10)
        #if center(0,0) -> 會被座標軸截到剩右下角1/4圓
        self.velocity = [randint(1,3),randint(3,6)]
        
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
        
    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
    def bounce(self):
        self.velocity[1] = -self.velocity[1]
    def revelocity(self):
        self.velocity = [0,0]
        v_x = 0
        while not v_x:
            v_x = randint(-3,3)
            
        else:
            self.velocity = [v_x,randint(3,6)]
        
    
