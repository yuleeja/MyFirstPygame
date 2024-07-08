import pygame
import random

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((640, 480))

pygame.display.set_caption('First Pygame')  # название приложения

icon = pygame.image.load('img/icon.png').convert_alpha()  # иконка приложения
pygame.display.set_icon(icon)

# фон
bg = pygame.image.load('img/bg.jpg').convert()
# gameover экран
gameover_img = pygame.image.load('img/gameover.jpg').convert()
gameover_img = pygame.transform.scale(gameover_img, (640, 480))

# Игрок
# движение влево
walk_left = [
    pygame.image.load('img/player_left/player_left1.png').convert_alpha(),
    pygame.image.load('img/player_left/player_left2.png').convert_alpha(),
    pygame.image.load('img/player_left/player_left3.png').convert_alpha(),
    pygame.image.load('img/player_left/player_left4.png').convert_alpha()
]
# движение вправо
walk_right = [
    pygame.image.load('img/player_right/player_right1.png').convert_alpha(),
    pygame.image.load('img/player_right/player_right2.png').convert_alpha(),
    pygame.image.load('img/player_right/player_right3.png').convert_alpha(),
    pygame.image.load('img/player_right/player_right4.png').convert_alpha()
]

enemy = pygame.image.load('img/enemy.png').convert_alpha()
enemy = pygame.transform.scale(enemy, (50, 50))

enemy_list_in_game = []

player_anim_count = 0
bg_x = 0

player_speed = 5
player_x = 150
player_y = 350

is_jump = False
jump_count = 9

bg_sound = pygame.mixer.Sound('sounds/main_theme.mp3')  # основная музыкальная тема
bg_sound.play(-1)  # в скобках указывается количество проигрываний(-1 - бесконечное проигрывание музыки)

enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 2500)

label = pygame.font.Font('fonts/Roboto-Black.ttf', 40)
restart_label = label.render('Try again', False, (247, 40, 66))
restart_label_rect = restart_label.get_rect(topleft=(240, 400))

# патроны
bullets_left = random.randint(1, 16)  # количество пуль
label_bullets_count = pygame.font.Font('fonts/Roboto-Black.ttf', 20)  # шрифт для отображения количества пуль
bullet = pygame.image.load('img/bullet.png').convert_alpha()
bullet = pygame.transform.scale(bullet, (25, 25))
bullets = []

gameplay = True

running = True
while running:

    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 640, 0))

    screen.blit(bullet, (15, 25))

    if gameplay:

        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))
        if enemy_list_in_game:
            for (i, el) in enumerate(enemy_list_in_game):
                screen.blit(enemy, el)
                el.x -= 10

                if el.x < -10:
                    enemy_list_in_game.pop(i)

                if player_rect.colliderect(el):  # отслеживаем соприкосновения квадратов игрока и врага
                    gameplay = False

        keys = pygame.key.get_pressed()  # получаем кнопку, на которую нажал пользователь

        # движения влево, вправо
        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))

        if keys[pygame.K_LEFT] and player_x > 50:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < 560:
            player_x += player_speed

        # прыжок
        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -9:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2

                jump_count -= 1
            else:
                is_jump = False
                jump_count = 9

        if player_anim_count == 3:
            player_anim_count = 0
        else:
            player_anim_count += 1

        bg_x -= 2
        if bg_x == -640:
            bg_x = 0

        # стрельба
        if bullets:
            for (i, el) in enumerate(bullets):
                screen.blit(bullet, (el.x, el.y))
                el.x += 4

                if el.x > 650:
                    bullets.pop(i)

                if enemy_list_in_game:
                    for (index, enemy_el) in enumerate(enemy_list_in_game):
                        if el.colliderect(enemy_el):
                            enemy_list_in_game.pop(index)
                            bullets.pop(i)

            # отображение количества выстрелов
            bullets_label = label_bullets_count.render(f'{bullets_left}', False, (247, 40, 66))
            screen.blit(bullets_label, (45, 25))

        # game over
    else:
        screen.blit(gameover_img, (0, 0))
        pygame.mixer.pause()
        screen.blit(restart_label, restart_label_rect)

        # restart game
        mouse = pygame.mouse.get_pos()  # определяем, где находится мышка
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:  # .get_pressed()[0] - нажатие ЛКM
            gameplay = True
            bg_sound.play(-1)
            player_x = 150
            enemy_list_in_game.clear()
            bullets.clear()
            bullets_left = random.randint(1, 16)

    pygame.display.update()

    # создание врагов
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == enemy_timer:
            enemy_list_in_game.append(enemy.get_rect(topleft=(642, 355)))

        # одиночный выстрел
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_b and bullets_left > 0:
            bullets.append(bullet.get_rect(topleft=(player_x + 30, player_y + 10)))
            bullets_left -= 1

    clock.tick(15)
