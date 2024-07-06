import pygame

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((640, 480))

pygame.display.set_caption('First Pygame')  # название приложения

icon = pygame.image.load('img/icon.png')  # иконка приложения
pygame.display.set_icon(icon)

bg = pygame.image.load('img/bg.jpg')

#движение влево
walk_left = [
    pygame.image.load('img/player_left/player_left1.png'),
    pygame.image.load('img/player_left/player_left2.png'),
    pygame.image.load('img/player_left/player_left3.png'),
    pygame.image.load('img/player_left/player_left4.png')
]
#движение вправо
walk_right = [
    pygame.image.load('img/player_right/player_right1.png'),
    pygame.image.load('img/player_right/player_right2.png'),
    pygame.image.load('img/player_right/player_right3.png'),
    pygame.image.load('img/player_right/player_right4.png')
]

player_anim_count = 0
bg_x = 0

player_speed = 5
player_x = 150
player_y = 350

is_jump = False
jump_count = 7

bg_sound = pygame.mixer.Sound('sounds/main_theme.mp3') #основная музыкальная тема
bg_sound.play()

running = True
while running:

    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 640, 0))

    keys = pygame.key.get_pressed()  # получаем кнопку, на которую нажал пользователь

    if keys[pygame.K_LEFT]:
        screen.blit(walk_left[player_anim_count], (player_x, player_y))
    else:
        screen.blit(walk_right[player_anim_count], (player_x, player_y))

    if keys[pygame.K_LEFT] and player_x > 50:
        player_x -= player_speed
    elif keys[pygame.K_RIGHT] and player_x < 560:
        player_x += player_speed

    if not is_jump:
        if keys[pygame.K_SPACE]:
            is_jump = True
    else:
        if jump_count >= -7:
            if jump_count > 0:
                player_y -= (jump_count ** 2) / 2
            else:
                player_y += (jump_count ** 2) / 2

            jump_count -= 1
        else:
            is_jump = False
            jump_count = 7

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
