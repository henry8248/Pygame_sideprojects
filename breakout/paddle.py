import pygame
BLACK = (0,0,0)

class Paddle(pygame.sprite.Sprite): #inherit from pygame Sprite class
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        super().__init__()

        #Pass in the color of the paddle, its width and height.
        #Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height]) #設定sprite長寬
        self.image.fill(BLACK)  #設定sprite顏色
        self.image.set_colorkey(BLACK)
        #pixels that have the same color as the colorkey will be transparent.

        #Draw the paddle (a rectangle!)  surface to draw on: self.image
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        #Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
    def moveLeft(self, pixels):
        self.rect.x -= pixels
        #check boundary
        if self.rect.x < 0:
            self.rect.x = 0
    def moveRight(self, pixels):
        self.rect.x += pixels
        if self.rect.x > 700: #self.rect.with = 100
            self.rect.x = 700

#Class is like a mould. It enables you to create as many objects as you need
#using the same mould.

#screen is the Surface object representing the application window
#img    is the Surface object of the image to display
#rect   is the Rect object which is the bounding rectangle of the image
