
import pygame

pygame.init()

screen = pygame.display.set_mode((864, 936))
pygame.display.set_caption("FALLPY (FLAPPY) BIRD")

WIDTH = 864
HEIGHT = 936

fps = 60
clock = pygame.time.Clock()

groundScroll = 0
scrollSpeed = 4
flying = False
gameover = False

bg = pygame.image.load("img/bg.png")
ground = pygame.image.load("img/ground.png")

run = True

class Flappy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for i in range(1,4):
            img = pygame.image.load(f"img/bird{i}.png")
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.velocity = 0
        self.clicked = False

    def update(self):
        if flying == True:
            self.velocity += 0.5
            if self.velocity > 8:
                self.velocity = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.velocity)
        
        if gameover == False:
            if self.clicked == False and pygame.mouse.get_pressed()[0] == 1:
                self.clicked = True
                self.velocity = -10
            #if pygame.mouse.get_pressed()[0] == 0:
            #    self.clicked = False
            self.counter += 1
            flapCooldown = 5
            if self.counter > flapCooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]
            self.image = pygame.transform.rotate(self.images[self.index], self.velocity * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)


birdGroup = pygame.sprite.Group()

flappyBird = Flappy(100, HEIGHT//2)
birdGroup.add(flappyBird)

while run:
    clock.tick(fps)
    screen.blit(bg, (0, 0))
    screen.blit(ground, (groundScroll, 768))

    # - drawing the bird group
    birdGroup.draw(screen)
    birdGroup.update()

    # - checking if bird hit the ground
    if flappyBird.rect.bottom > 768:
        gameover = True
        flying = False
    
    # - if not gameover
    if gameover == False:
        # - making the ground scroll / move
        groundScroll -= scrollSpeed
        if abs(groundScroll) > 35:
            groundScroll = 0

    # - quit function
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and gameover == False:
            flying = True

    pygame.display.update()

pygame.quit()