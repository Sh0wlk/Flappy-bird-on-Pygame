import pygame
import random
from os import path
import sys

img_dir = path.join(path.dirname(__file__), 'img')

WIDTH = 900
HEIGHT = 504
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
COLB = (246, 246, 246)
COLBB = (246, 242, 243)
# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("flappy bird")
clock = pygame.time.Clock()
font_name = pygame.font.match_font('arial')
posx = [1500, 1900, 2300, 2700, 3100]
posy = [-250, -225, 375, 400, 425]

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

background = pygame.image.load(path.join(img_dir, "sky.png")).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background1_rect = background.get_rect()
background2_rect = background.get_rect()
background2_rect.x = WIDTH

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(player_img, (40, 30))
        self.image_orig = pygame.transform.scale(player_img, (40, 30))
        self.image.set_colorkey(COLB)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2 - 200
        self.rect.bottom = HEIGHT / 2
        self.gravity = 1  # Гравитация
        self.jump_strength = 12  # Сила прыжка
        self.is_jumping = False  # Признак прыжка
        self.speed_y = 0  # Скорость по оси Y
        self.rot = 30
        self.rot_speed = -7
        self.last_update = pygame.time.get_ticks()

    def update(self):
        # Логика прыжка
        if self.is_jumping:
            now = pygame.time.get_ticks()
            if now - self.last_update > 50:
                self.last_update = now
                self.rot = (self.rot + self.rot_speed)
                new_image = pygame.transform.rotate(self.image_orig, self.rot)
                old_center = self.rect.center
                self.image = new_image
                self.image.set_colorkey(COLB)
                self.rect = self.image.get_rect()
                self.rect.center = old_center
            self.speed_y += self.gravity  # Применяем гравитацию
            self.rect.y += self.speed_y  # Обновляем позицию по Y

            # Проверка на приземление
            if pygame.key.get_pressed()[pygame.K_SPACE]:  # Проверка на уровень земли
                self.is_jumping = False  # Не в воздухе
                self.speed_y = 0  # Сброс скорости падения
                self.speed_y += self.gravity  # Применяем гравитацию
                self.rect.y += self.speed_y
                self.is_jumping = True
                self.rot = 30
                self.speed_y = -self.jump_strength
        else:
            # Проверка на прыжок
            if pygame.key.get_pressed()[pygame.K_SPACE]:  # Прыжок по пробелу
                self.is_jumping = True
                self.speed_y = -self.jump_strength
        if self.rect.top > HEIGHT or self.rect.top < 0:
            running = false


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pipe_img, (200  , 350))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.spawn_position()
        self.speed_x = 4
        self.flipped = False
        self.rect.x = 1000
        if self.rect.y < 0:
            self.image = pygame.transform.flip(self.image, False, True)
            self.flipped = True

    def spawn_position(self):
        placed = False
        while not placed:
            # Выбираем случайные координаты
            self.rect.x = random.choice(posx)
            self.rect.y = random.choice(posy)

            # Проверяем, пересекает ли этот враг другие враги в группе
            if not pygame.sprite.spritecollideany(self, mobs):
                placed = True

    def update(self):
        global score
        self.rect.x -= self.speed_x
        if self.rect.x < -300:
            self.rect.x = random.choice(posx)
            if self.rect.x == posx[1]:
                self.rect.y = random.choice(posy)
            elif self.rect.x == posx[2]:
                self.rect.y = random.choice(posy)
            elif self.rect.x == posx[3]:
                self.rect.y = random.choice(posy)
            elif self.rect.x == posx[4]:
                self.rect.y = random.choice(posy)
            elif self.rect.x == posx[0]:
                self.rect.y = random.choice(posy)
            if self.rect.y < 0:
                if self.flipped == True:
                    self.flipped = True
                else:
                    self.image = pygame.transform.flip(self.image, False, True)
                    self.flipped = True
            else:
                if self.flipped == False:
                    self.flipped = False
                else:
                    self.image = pygame.transform.flip(self.image, False, True)
                    self.flipped = False

player_img = pygame.image.load(path.join(img_dir, "bird.png")).convert()
pipe_img = pygame.image .load(path.join(img_dir, "pipe.png")).convert()

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

mobs = pygame.sprite.Group()
for i in range(6):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
mobs = pygame.sprite.Group()
for i in range(6):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
score = 0

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    background1_rect.x -= 3
    background2_rect.x -= 3

    # Проверка границы и сброс позиции
    if background1_rect.x < -WIDTH:
        background1_rect.x = WIDTH-5
    if background2_rect.x < -WIDTH:
        background2_rect.x = WIDTH-5
    all_sprites.update()

    hits = pygame.sprite.spritecollide(player, mobs, False)
    if hits:
        running = False

    for mob in mobs:
        if mob.rect.x == -300:
            score += 100

    screen.fill(BLACK)
    screen.blit(background, background1_rect)
    screen.blit(background, background2_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    pygame.display.flip()

pygame.quit()