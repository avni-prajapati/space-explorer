import pygame
import random
from pygame import mixer

# Initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((1000, 800))  # (breadth,height)

# background
background = pygame.image.load('space.png')

# Background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Explorer")
icon = pygame.image.load('icon.png')
pygame.display.set_icon((icon))

# player
playerimage = pygame.image.load('spaceship.png')
playerX = 430
playerY = 600
playerX_change = 0

# Enemy
enemyimage = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemy = 6
for i in range(no_of_enemy):
    enemyimage.append(pygame.image.load('monster.png'))
    enemyX.append(random.randint(20, 980))  # 460
    enemyY.append(random.randint(50, 150))  # 50
    enemyX_change.append(0.2)
    enemyY_change.append(30)

# Bullet
# Ready - you cant see bullet on the screen
# Fire - The bullet is currently moving
bulletimage = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 600
bulletX_change = 0
bulletY_change = 1
bullet_state = 'ready'

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# game over
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render('Score : ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text(x=500,y=400):
    over_text = over_font.render('Game Over',True, (255, 255, 255))
    screen.blit(over_text,(300,300))

def player(x, y):
    screen.blit(playerimage, (x, y))  # ufo


def enemy(x, y, i):
    screen.blit(enemyimage[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletimage, (x + 50, y + 50))  # illusion its coming from ship


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = (((enemyX - bulletX) ** 2 + (enemyY - bulletY) ** 2)) ** (1 / 2)
    if distance < 60:
        return True
    else:
        return False


# Game loop
running = True
while running:
    screen.fill((0, 0, 50))  # bg color RGB
    # background img
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed and which it is
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.4
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.4
            if event.key == pygame.K_SPACE:
                bullet_sound = mixer.Sound('laser.wav')
                bullet_sound.play()
                if bullet_state == 'ready':
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 872:  # pixel value (breadth-pixel) 1000-128=872
        playerX = 872

    for i in range(no_of_enemy):

        # game over
        if enemyY[i] > 550:
            for j in range(no_of_enemy):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 936:  # pixel value (breadth-pixel) 1000-128=872
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explotion_sound = mixer.Sound('explosion.wav')
            explotion_sound.play()
            bulletY = 600
            bullet_state = 'ready'
            score_value += 1
            enemyX[i] = random.randint(20, 980)  # 460
            enemyY[i] = random.randint(50, 150)  # 50

        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 600
        bullet_state = ('ready')

    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
