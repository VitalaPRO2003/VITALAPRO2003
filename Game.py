import pygame
import sys
import os
import Platformes
from Player import Character
import Enemies
pygame.init()
pygame.mixer.init()



def main():
    Level(load_level('level.txt'), 90)
    level_complete()
    Level(load_level('level2.txt'), 30)
    level_complete()
    Level(load_level('level3.txt'), 60)
    win()


def load_level(filename):
    filename = "data/" + filename
    try:
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
    except FileNotFoundError as message:
        print('такого файлу не існує ', filename)
        raise SystemExit()

    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def initialize():
    global screen, WIDTH, HEIGHT
    WIDTH, HEIGHT = 1024, 512
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Super Mario Bros.')




    main_menu()


def main_menu():
    pygame.mixer.Sound('data\\main_menu.ogg').play(-1)
    image_start = load_image('start_btn1.png')
    image_exit = load_image('exit_btn1.png')
    background = load_image('main_menu.png')
    continues = True
    while continues:
        screen.blit(background, (0, 0))
        screen.blit(image_start, (412, 250))
        screen.blit(image_exit, (434, 350))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEMOTION:
                if 412 < event.pos[0] < 612 and 250 < event.pos[1] < 316:
                    image_start = load_image('start_btn2.png')
                else:
                    image_start = load_image('start_btn1.png')
                if 434 < event.pos[0] < 590 and 350 < event.pos[1] < 416:
                    image_exit = load_image('exit_btn2.png')
                else:
                    image_exit = load_image('exit_btn1.png')
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 412 < event.pos[0] < 612 and 250 < event.pos[1] < 316:
                    pygame.mixer.stop()
                    continues = False
                if 434 < event.pos[0] < 590 and 350 < event.pos[1] < 416:
                    terminate()
        screen.blit(background, (0, 0))
        screen.blit(image_start, (412, 250))
        screen.blit(image_exit, (434, 350))
        pygame.display.flip()
    main()


def game_over():
    pygame.mixer.stop()
    pygame.mixer.Sound('data\\game_over.wav').play()
    image = pygame.transform.scale(load_image('game_over.png'), (1024, 512))
    image_menu = load_image('menu_btn1.png')
    continues = True
    while continues:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 368 < event.pos[0] < 656 and 390 < event.pos[1] < 456:
                    pygame.mixer.stop()
                    continues = False
            if event.type == pygame.MOUSEMOTION:
                if 368 < event.pos[0] < 656 and 390 < event.pos[1] < 456:
                    image_menu = load_image('menu_btn2.png')
                else:
                    image_menu = load_image('menu_btn1.png')
            if event.type == pygame.QUIT:
                terminate()
        screen.blit(image, (0, 0))
        screen.blit(image_menu, (368, 390))
        pygame.display.flip()
    main_menu()


def level_complete():
    pygame.mixer.stop()
    image = load_image('level_complete.png')
    screen.blit(image, (0, 0))
    pygame.display.flip()
    music = pygame.mixer.Sound('data\\level_complete.wav')
    music.play()
    pygame.time.wait(int(music.get_length() * 1000))
    pygame.mixer.stop()


def win():
    pygame.mixer.stop()
    image = load_image('win.png')
    screen.blit(image, (0, 0))
    pygame.display.flip()
    music = pygame.mixer.Sound('data\\win.wav')
    music.play()
    continues = True
    while continues:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                continues = False
    main_menu()


def terminate():
    pygame.mixer.quit()
    pygame.quit()
    sys.exit()



def camera_configure(camera, target_rect):
    l = -target_rect.x + WIDTH/2
    t = -target_rect.y + HEIGHT/2
    w, h = camera.width, camera.height

    l = min(0, l)
    l = max(-(w - WIDTH), l)
    t = max(-(h - HEIGHT), t)
    t = min(0, t)

    return pygame.Rect(l, t, w, h)



class Level:
    def __init__(self, level, time_in_sec):

        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.flag = pygame.sprite.Group()
        self.hero = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.participles = pygame.sprite.Group()
        self.finish = pygame.sprite.Group()
        self.secret_blocks = pygame.sprite.Group()

        self.player, level_length_width, level_length_height = self.generate_level(level, time_in_sec)

        total_level_width = level_length_width * 32
        total_level_height = level_length_height * 32
        self.camera = Camera(camera_configure, total_level_width, total_level_height)

        self.clock = pygame.time.Clock()
        self.background = load_image('background.png')
        self.music = pygame.mixer.Sound('data\\mario_theme.ogg')

        self.play()


    def generate_level(self, level, time_in_sec):
        x = 0
        y = 0
        player = None
        for row in level:
            for col in row:
                if col == '-':
                    Platformes.Platform('platform', self.all_sprites, self.platforms, x, y)
                if col == 'M':
                    player = Character(self.all_sprites, self.hero, x, y, time_in_sec)
                if col == 'B':
                    Platformes.Platform('block', self.all_sprites, self.platforms, x, y)
                if col == 'L':
                    Platformes.Platform('ladder', self.all_sprites, self.platforms, x, y)
                if col == '?':
                    Platformes.SecretBlock('secret_block', self.all_sprites, self.platforms, self.secret_blocks, x, y)
                if col == 't':
                    Platformes.Platform('pipe_L', self.all_sprites, self.platforms, x, y)
                if col == 'y':
                    Platformes.Platform('pipe_R', self.all_sprites, self.platforms, x, y)
                if col == 'T':
                    Platformes.Platform('pipe_TL', self.all_sprites, self.platforms, x, y)
                if col == 'Y':
                    Platformes.Platform('pipe_TR', self.all_sprites, self.platforms, x, y)
                if col == 'I':
                    Platformes.NotObstacle('flag_I', self.all_sprites, x, y)
                if col == 'O':
                    Platformes.NotObstacle('flag_O', self.all_sprites, x, y)
                if col == 'F':
                    Platformes.NotObstacle('flag_I', self.all_sprites, x, y)
                    Platformes.NotObstacle('flag_F', self.all_sprites, x - 16, y)
                if col == 'G':
                    Enemies.Grib(self.all_sprites, self.enemies, x, y)
                if col == '*':
                    Platformes.Castle('castle', self.all_sprites, self.finish, x, y)
                x += 32
            y += 32
            x = 0
        return player, len(level[0]), len(level)

    def play(self):
        self.music.play(-1)
        left = False
        right = False
        up = False
        continues = True
        gameover = False
        while continues:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        left = True
                    elif event.key == pygame.K_RIGHT:
                        right = True
                    elif event.key == pygame.K_UP:
                        up = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        left = False
                    elif event.key == pygame.K_RIGHT:
                        right = False
                    elif event.key == pygame.K_UP:
                        up = False
            screen.blit(self.background, (0, 0))
            self.player.update(left, right, up, self.platforms, self.enemies,
                               self.participles, self.secret_blocks, screen)
            self.enemies.update(self.platforms, self.enemies)
            self.participles.update(self.camera.state)
            self.camera.update(self.player)
            for sprite in self.all_sprites:
                if self.player.rect.x - 1024 < sprite.rect.x < self.player.rect.x + 1024:  # оптимизация игры))
                    screen.blit(sprite.image, self.camera.apply(sprite))
            self.player.draw_UI(screen)
            self.clock.tick(60)
            pygame.display.flip()
            if pygame.sprite.spritecollideany(self.player, self.finish):
                continues = False
            if self.player.lifes == 0:
                continues = False
                gameover = True
            if self.player.timer <= 0:
                continues = False
                gameover = True
        if gameover:
            game_over()



class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)



initialize()
start_screen()
