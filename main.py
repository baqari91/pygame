import pygame
import sys
from pygame import mixer
import random

clock = pygame.time.Clock()
fps = 60

mixer.init()
pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Arial', 36)
info = pygame.display.Info()
width = info.current_w
height = info.current_h
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Shooter")

# RGB RED GREEN BLUE
red = (255, 100, 100)
green = (100, 255, 100)


background_image = pygame.transform.scale(pygame.image.load("background.jpg"), (width, height))
player_image = pygame.image.load("space-ship.png")
enemy_image = pygame.image.load("enemy.png")
bullet_image = pygame.image.load("bullet.png")


class Player:
    def __init__(self, speed, size, health, image):
        self.size = size
        self.image = pygame.transform.scale(image, (self.size, self.size))
        self.current_image = self.image
        self.rect = pygame.Rect(width/2, height/2, self.size, self.size)
        self.rect.center = [width/2, height/4]
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

        # საზღვრის დაწესება
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= width:
            self.rect.right = width
        if self.rect.top <= height/2 + self.size:
            self.rect.top = height/2 + self.size
        if self.rect.bottom >= height:
            self.rect.bottom = height

    def update(self):
        self.draw_player()
        self.move_player()


class Bullet:
    def __init__(self, x, y, speed, image):
        self.image = pygame.transform.scale(image, (36, 36))  # Adjust size as needed
        self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed

    def update(self):
        self.rect.y -= self.speed
        screen.blit(self.image, self.rect)

        # Check collision with enemies
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):  # Check for collision between bullet and enemy
                # Handle collision logic here (e.g., decrease enemy health, remove bullet)
                enemies.remove(enemy)
                player_bullets.remove(self)  # Remove the bullet on collision


class EnemyBullet(Bullet):
    def update(self):
        self.rect.y += self.speed
        screen.blit(self.image, self.rect)

        if self.rect.colliderect(player.rect):
            var = player.health - 1



class Enemy:
    def __init__(self, speed, size, health, image):
        self.size = size
        self.image = pygame.transform.scale(image, (self.size, self.size))
        self.current_image = self.image
        self.speed = speed
        self.rect = self.image.get_rect()

        self.rect.x = random.randint(0, width - self.size)
        self.rect.y = random.randint(0, height // 2 - self.size)

        self.speed = speed
        self.health = health

    def draw_enemy(self):
        screen.blit(self.current_image, (self.rect.x, self.rect.y))

    def move_enemy(self):
        self.rect.x += self.speed
        if self.rect.x > width:
            self.rect.y = random.randint(0, height//2 - self.size)
            self.rect.x = random.randint(-width, -self.size)

    def shoot(self):
        bullet = EnemyBullet(self.rect.centerx, self.rect.bottom, 5, bullet_image)  # Create a bullet below the enemy
        enemy_bullets.append(bullet)  # Add bullet to the list

    def update(self):
        self.draw_enemy()
        self.move_enemy()



class EnemyRight(Enemy):
    def move_enemy(self):
        self.rect.width -= self.speed
        if self.rect.width == self.rect.x:
            self.rect.y - random.randint(0, height//2 - self.size)
            self.rect.x = random.randint(-width, -self.size)






def player_shoot():
    bullet = Bullet(player.rect.centerx, player.rect.y, 20, bullet_image)  # Create bullet at player's position
    player_bullets.append(bullet)  # Add bullet to the list


def show_health():
    health_text = font.render(f'Health: {player.health}', True, (255, 255, 255))
    screen.blit(health_text, (10, 10))



enemy_bullets = []  # List to store enemy bullets
player_bullets = []  # List to store player's bullets

enemy1 = Enemy(10, 60, 100, enemy_image)
enemy2 = Enemy(10, 60, 100, enemy_image)
enemy3 = Enemy(10, 60, 100, enemy_image)
enemy4 = Enemy(10, 60, 100, enemy_image)
enemy5 = Enemy(-10, 60, 100, enemy_image)

enemies = [enemy1, enemy2, enemy3, enemy4, enemy5]  # List to store enemy instances

player = Player(10, 60, 100, player_image)


run = True
while run:
    clock.tick(fps)
    # screen.fill(red)
    screen.blit(background_image, (0, 0))
    player.update()
    show_health()

    for enemy in enemies:
        enemy.update()
        if random.randint(1, 100) == 1:  # Adjust this probability to control enemy firing rate
            enemy.shoot()


    for bullet in enemy_bullets:
        bullet.update()
        for bullet in enemy_bullets[:]:  # Iterate over a copy of the list to avoid modifying it during iteration
            bullet.update()
            if bullet.rect.bottom < 0:
              enemy_bullets.remove(bullet)

    for bullet in player_bullets:
        bullet.update()
        for bullet in player_bullets[:]:  # Iterate over a copy of the list to avoid modifying it during iteration
            bullet.update()
            if bullet.rect.bottom < 0:
                player_bullets.remove(bullet)

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
            if event.key == pygame.K_SPACE:
                player_shoot()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                player.cur_speed_w = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or event.key == pygame.K_s:
                player.cur_speed_h = 0

    pygame.display.update()

pygame.quit()
sys.exit()