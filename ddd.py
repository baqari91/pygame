import pygame
import sys
from pygame import mixer
import random

clock = pygame.time.Clock()
fps = 60

mixer.init()
pygame.init()

info = pygame.display.Info()

width = info.current_w
height = info.current_h

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Shooter")

#RGB RED GREEN BLUE
red = (255, 100, 100)
green = (100, 255, 100)


player_image = pygame.image.load("space-ship.png")
enemy_image = pygame.image.load("enemy.png")
background_image = pygame.transform.scale(pygame.image.load("background.jpg"), (width, height))



class Player:
    def __init__(self, speed, size, health, image):
        self.size = size
        self.image = pygame.transform.scale(image, (self.size, self.size))
        self.current_image = self.image
        self.rect = pygame.Rect(width/2, height/2, self.size, self.size)
        self.rect.center = [width/2, height/2]
        self.speed = speed
        self.cur_speed_w = 0
        self.cur_speed_h = 0
        self.health = health


    def draw_player(self):
        if self.cur_speed_w < 0:
            self.current_image = pygame.transform.flip(self.image, True, False)
        if self.cur_speed_w > 0:
            self.current_image = self.image




        # pygame.draw.rect(screen, green, self.rect)
        screen.blit(self.current_image, (self.rect.x, self.rect.y))

    def move_player(self):
        self.rect.x += self.cur_speed_w
        self.rect.y += self.cur_speed_h

        #საზღვრის დაწესება
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= width:
            self.rect.right = width
        if self.rect.top <= height/2:
            self.rect.top = height/2
        if self.rect.bottom >= height:
            self.rect.bottom = height

    def update(self):
        self.draw_player()
        self.move_player()


class Enemy:
    def __init__(self, speed, size, health, image):
        self.size = size
        self.image = pygame.transform.scale(image, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, width - self.size)
        # self.rect.y = random.randint(0, height / 2 - self.size)  # Adjust as needed
        self.speed = speed
        self.health = health

    def draw_enemy(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def move_enemy(self):
        self.rect.y += self.speed
        if self.rect.y > height:
            self.rect.x = random.randint(0, width - self.size)
            self.rect.y = random.randint(-height, -self.size)

    def update(self):
        self.draw_enemy()
        self.move_enemy()


enemies = []  # List to store enemy instances

player = Player(10, 60, 100, player_image)
enemy = Enemy(10, 60, 100, enemy_image)


run = True
while run:
    clock.tick(fps)
    # screen.fill(red)
    screen.blit(background_image, (0, 0))
    player.update()

    for enemy in enemies:
        enemy.update()




    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.cur_speed_w = -player.speed
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.cur_speed_w = player.speed
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                player.cur_speed_h = -player.speed
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player.cur_speed_h = player.speed

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                player.cur_speed_w = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or event.key == pygame.K_s:
                player.cur_speed_h = 0

    pygame.display.update()

pygame.quit()
sys.exit()