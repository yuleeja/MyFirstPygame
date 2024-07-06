import pygame

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((640, 480))

pygame.display.set_caption('First Pygame')  # название приложения

icon = pygame.image.load('img/icon.png')  # иконка приложения
pygame.display.set_icon(icon)

bg = pygame.image.load('img/bg.jpg')

walk_left = [
    pygame.image.load('img/player_left/player_left1.png'),
    pygame.image.load('img/player_left/player_left2.png'),
    pygame.image.load('img/player_left/player_left3.png'),
    pygame.image.load('img/player_left/player_left4.png')
]

walk_right = [
    pygame.image.load('img/player_right/player_right1.png'),
    pygame.image.load('img/player_right/player_right2.png'),
    pygame.image.load('img/player_right/player_right3.png'),
    pygame.image.load('img/player_right/player_right4.png')
]

player_anim_count = 0
bg_x = 0

bg_sound = pygame.mixer.Sound('sounds/main_theme.mp3')
bg_sound.play()

running = True
while running:

    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 640, 0))
    screen.blit(walk_right[player_anim_count], (300, 340))



    if player_anim_count == 3:
        player_anim_count = 0
    else:
        player_anim_count += 1

    bg_x -= 2
    if bg_x == -640:
        bg_x = 0

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    clock.tick(15)
