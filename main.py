import pygame
import random
import sys
from pygame import mixer

pygame.init()
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
game_over = False
paused = False
running = True

# Loading Bar
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Background
background = pygame.image.load("space.jpg")
background = pygame.transform.rotozoom(background, 0, 1.7)
mixer.music.load("background.wav")
mixer.music.set_volume(0.2)
mixer.music.play(-1)

# Game over background
game_over_font = pygame.font.Font("freesansbold.ttf", 64)

# Player
player_icon = pygame.image.load("spaceship.png")
player_width = 50
player_height = 30
player_icon = pygame.transform.smoothscale(player_icon, (player_width, player_height))
player_x = 370
player_y = 560
player_x_change = 0

# Alien
aliens = pygame.sprite.Group()
alien_y_change = 1
spawn_alien = pygame.USEREVENT
pygame.time.set_timer(spawn_alien, 1000)

# Lasers
lasers = pygame.sprite.Group()
laser_y_change = 0.5

# Score
score = 0
score_font = pygame.font.Font("freesansbold.ttf", 16)
score_x = 10
score_y = 10


def player(x, y):
    screen.blit(player_icon, (x, y))


def create_alien():
    aw = 50
    return Alien(random.randint(0, width - aw), 0)


def create_laser():
    return Laser(player_x + 24, player_y - 5)


def display_score(x, y):
    score_value = score_font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_value, (x, y))


def game_over_text():
    global paused
    paused = True
    game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(game_over_text, (width / 2 - 185, height / 2 - 100))
    mixer.music.stop()
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


class Alien(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        aw = 50
        ah = 30
        self.image = pygame.image.load("ufo.png")
        self.image = pygame.transform.smoothscale(self.image, (aw, ah))
        self.rect = self.image.get_rect(center=(pos_x, pos_y))

    def update(self):
        global game_over
        ah = 30
        self.rect.y += alien_y_change
        if self.rect.y == height - ah:
            game_over = True


class Laser(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.Surface((5, 30))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(pos_x, pos_y))

    def update(self):
        self.rect.y -= laser_y_change
        if self.rect.y <= 0:
            self.kill()


while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    if game_over:
        game_over_text()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        player_x_change = 0
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_RIGHT]:
            player_x_change = 3
        if pressed[pygame.K_LEFT]:
            player_x_change = -3
        if pressed[pygame.K_SPACE]:
            lasers.add(create_laser())
            laser_sound = mixer.Sound("laser.wav")
            laser_sound.play()
            laser_sound.set_volume(0.2)
        if pressed[pygame.K_LEFT] and pressed[pygame.K_RIGHT]:
            player_x_change = 0
        if event.type == spawn_alien:
            aliens.add(create_alien())

    player_x += player_x_change

    if player_x <= 0:
        player_x = 0
    elif player_x >= width - player_width:
        player_x = width - player_width

    for a in aliens:
        a.update()
        if pygame.sprite.groupcollide(aliens, lasers, True, True):
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            explosion_sound.set_volume(0.2)
            score += 1

    display_score(score_x, score_y)
    player(player_x, player_y)
    aliens.draw(screen)
    lasers.draw(screen)
    lasers.update()
    pygame.display.update()
