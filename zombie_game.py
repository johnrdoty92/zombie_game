import pygame, sys, os, random, time
from pygame.locals import *

pygame.init()

# Contants
SIZE = WIDTH, HEIGHT = (1000, 600)
DISPLAY = pygame.display.set_mode(SIZE)
FPS = pygame.time.Clock()
BASE_SPEED = 7
BASE_HEALTH = 300
RED_BG = pygame.Surface(SIZE)
RED_BG.fill((255,0,0))
GREEN = (0, 255, 0)
NORMAL_BG = pygame.image.load(os.path.join('Assets','GrassField.png')).convert()

FONT = pygame.font.SysFont('Arial', 60)
game_over_text = FONT.render(f"GAME OVER", True, (200,200,200))

background = NORMAL_BG
score = 0

# Classes
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprites = [
            pygame.image.load(os.path.join("Assets","Enemy_Standing.png")).convert_alpha(),
            pygame.image.load(os.path.join("Assets","Enemy_L_Step.png")).convert_alpha(),
            pygame.image.load(os.path.join("Assets","Enemy_Standing.png")).convert_alpha(),
            pygame.image.load(os.path.join("Assets","Enemy_R_Step.png")).convert_alpha()
        ]
        self.surface = pygame.Surface((100,150))
        self.rect = self.surface.get_rect(center = (random.randint(50, WIDTH-50), random.randint(75,HEIGHT-75)))
        self.x_speed = random.randint(1,5)
        self.y_speed = random.randint(1,5)
        self.direction = 1 #1 is 'right', -1 is 'left'
        self.step_count = 0
    
    def move(self):
        if self.step_count >= 59:
            self.step_count = 0
        self.rect.move_ip(self.x_speed, self.y_speed)
        if (self.rect.right > WIDTH) or (self.rect.left < 0):
            self.x_speed *= -1
            self.direction *= -1
        if (self.rect.bottom > HEIGHT) or (self.rect.top < 0):
            self.y_speed *= -1
        self.step_count += 1

class Hero(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprites = {
            'walking': [
            pygame.image.load(os.path.join("Assets", "Hero_Standing.png")).convert_alpha(),
            pygame.image.load(os.path.join("Assets", "Hero_R_Step.png")).convert_alpha(),
            pygame.image.load(os.path.join("Assets", "Hero_Standing.png")).convert_alpha(),
            pygame.image.load(os.path.join("Assets", "Hero_L_Step.png")).convert_alpha(),
            ],
            'hurt': pygame.image.load(os.path.join("Assets", "AvatarHurt.png")).convert_alpha()
        }
        self.surface = pygame.Surface((100,150))
        self.rect = self.surface.get_rect(center = (WIDTH/2, HEIGHT/2))
        self.x_speed = BASE_SPEED
        self.y_speed = BASE_SPEED
        self.health = BASE_HEALTH
        self.direction = 'right'
        self.step_count = 0

    def update_health(self):
        pygame.draw.rect(DISPLAY, GREEN, (20, 20, self.health, 20))
        if self.health < BASE_HEALTH:
            pygame.draw.rect(DISPLAY, (255,0,0), (self.health + 20, 20, BASE_HEALTH - self.health, 20))

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            if self.direction == 'right':
                self.step_count = 0
            self.direction = 'left'
            self.step_count += 1
            self.rect.move_ip(-BASE_SPEED, 0)
        if self.rect.right < WIDTH and pressed_keys[K_RIGHT]:
            if self.direction == 'left':
                self.step_count = 0
            self.direction = 'right'
            self.step_count += 1
            self.rect.move_ip(BASE_SPEED, 0)
        if self.rect.top > 0 and pressed_keys[K_UP]:
            self.rect.move_ip(0, -BASE_SPEED)
            self.step_count += 1
        if self.rect.bottom < HEIGHT and pressed_keys[K_DOWN]:
            self.rect.move_ip(0, BASE_SPEED)
            self.step_count += 1
        if self.step_count >= 59:
            self.step_count = 0


#Drawing the entire frame
def draw_window(display, background, normal_BG, damage_BG, hero_sprite, enemy_sprites):
    #Check for collision:
    if pygame.sprite.spritecollideany(hero_sprite, enemy_sprites):
        background = damage_BG
        hero_sprite.health -= 1
        current_hero_sprite = hero_sprite.sprites['hurt']
    else:
        background = normal_BG
        current_hero_sprite = hero_sprite.sprites['walking'][hero_sprite.step_count//15]
    #Draw the main background
    display.blit(background, (0,0))
    #Draw all the enemy sprites and move them
    for character in enemy_sprites:
        current_enemy_sprite = character.sprites[character.step_count//15]
        if character.direction == -1:
            current_enemy_sprite = pygame.transform.flip(current_enemy_sprite, True, False)
        display.blit(current_enemy_sprite, character.rect)
        character.move()
    #Draw hero sprite and move
    if hero_sprite.direction == 'left':
        current_hero_sprite = pygame.transform.flip(current_hero_sprite, True, False)
    display.blit(current_hero_sprite, hero_sprite.rect)
    hero_sprite.move()
    #Check health
    hero_sprite.update_health()
    if hero_sprite.health <= 0:
        game_over()
    #Draw current score
    score_text = FONT.render(f"TIME SURVIVED: {score//60}", True, (200,200,200))
    zombie_count_text = FONT.render(f"ZOMBIE COUNT: {zombie_count}", True, (200,200,200))
    display.blit(score_text, (20, HEIGHT - 20 - score_text.get_height()) )
    display.blit(zombie_count_text, (WIDTH/2, 20))
    pygame.display.update()
    FPS.tick(60)

#On lose
def game_over():
    DISPLAY.fill((0, 0, 0))
    DISPLAY.blit(game_over_text, (WIDTH/2 - (game_over_text.get_width()/2), HEIGHT/2 - game_over_text.get_height()/2))
    score_text = FONT.render(f"SURVIVED FOR {score//60} SECONDS", True, (200,200,200))
    zombie_count_text = FONT.render(f"ZOMBIE COUNT: {zombie_count}", True, (200,200,200))
    DISPLAY.blit(score_text, (WIDTH/2 - (score_text.get_width()/2), (HEIGHT/2 + score_text.get_height() * 1.5)))
    DISPLAY.blit(zombie_count_text, (WIDTH/2 - (zombie_count_text.get_width()/2), (HEIGHT/2 + zombie_count_text.get_height() * 2.5)))
    for character in all_sprites:
        character.kill()
    pygame.display.update()
    time.sleep(2)
    pygame.quit()
    sys.exit()

# User Events
SPAWN_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_ENEMY, 7000)

# Initialize Sprites
zombie = Enemy()
hero = Hero()
zombie_count = 1
# Sprite Groups
enemies = pygame.sprite.Group()
enemies.add(zombie)
all_sprites = pygame.sprite.Group()
all_sprites.add(zombie)
all_sprites.add(hero)

# Game Loop
while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SPAWN_ENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
            zombie_count += 1
    score += 1
    draw_window(DISPLAY, background, NORMAL_BG, RED_BG, hero, enemies)
    