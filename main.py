import pygame
from sys import exit

RESOLUTION = (400,800)
BG_COLOR = 'pink'
HERO_COLOR = 'red'
WALL_COLOR = 'black'
GRAVITY = 0.25
JUMP_STRENGTH = 10

class Hero(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50,50))
        self.image.fill(HERO_COLOR)
        self.rect = self.image.get_rect(midbottom=(200,300))
        self.velocity = pygame.math.Vector2(0,0)
        self.jumps = 0


class Wall(pygame.sprite.Sprite):
    def __init__(self,wall):
        super().__init__()
        self.image = pygame.Surface(wall['size'])
        self.image.fill(WALL_COLOR)
        self.rect = self.image.get_rect(topleft=wall['pos'])
        
WALL_LIST = [
#         ширина высота  слева сверху
#             ↓  ↓           ↓ ↓
    {'size':(400,15), 'pos':(0,600)}, # down
    {'size':(100,15), 'pos':(100,400)}, # down

]



pygame.init()
screen = pygame.display.set_mode(RESOLUTION)
clock = pygame.time.Clock()

bg_surface = pygame.Surface(RESOLUTION)
bg_surface.fill(BG_COLOR)

ground_surface = pygame.Surface((400,250))
ground_surface.fill("#646400")

giovanni = Hero()
hero_sprites = pygame.sprite.Group()
hero_sprites.add(giovanni)

wall_sprites = pygame.sprite.Group()
for o in WALL_LIST:
    new_wall = Wall(o)
    wall_sprites.add(new_wall)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_SPACE or event.key == pygame.K_w) and (giovanni.jumps > 0):
                giovanni.velocity.y = - JUMP_STRENGTH
                giovanni.jumps -= 1

    keys = pygame.key.get_pressed()

    giovanni.velocity.x = 0

    if keys[pygame.K_a]:
        giovanni.velocity += pygame.math.Vector2(-3,0)
    if keys[pygame.K_d]:
        giovanni.velocity += pygame.math.Vector2(+3,0)

    giovanni.velocity.y += GRAVITY

    giovanni.rect.move_ip(giovanni.velocity)

    for platform in wall_sprites:
        if giovanni.rect.colliderect(platform.rect) and giovanni.velocity.y > 0:
            giovanni.jumps = 2
            giovanni.velocity.y = 0
            giovanni.rect.bottom = platform.rect.y

    screen.blit(bg_surface,(0,0))

    screen.blit(ground_surface,(0,600))
    hero_sprites.draw(screen)
    wall_sprites.draw(screen)


    pygame.display.update()
    clock.tick(60)