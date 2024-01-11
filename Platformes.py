import pygame
# картинки каждого объекта
images = {'platform': pygame.image.load('data\\platforms\\platform.png'),
          'block': pygame.image.load('data\\platforms\\block.png'),
          'ladder': pygame.image.load('data\\platforms\\ladder.png'),
          'secret_block': pygame.image.load('data\\platforms\\secret_block.png'),
          'activated_sblock': pygame.image.load('data\\platforms\\secret_block2.png'),
          'pipe_L': pygame.image.load('data\\platforms\\pipe_L.png'),
          'pipe_R': pygame.image.load('data\\platforms\\pipe_R.png'),
          'pipe_TL': pygame.image.load('data\\platforms\\pipe_TL.png'),
          'pipe_TR': pygame.image.load('data\\platforms\\pipe_TR.png'),
          'flag_I': pygame.image.load('data\\platforms\\flag_I.png'),
          'flag_O': pygame.image.load('data\\platforms\\flag_O.png'),
          'flag_F': pygame.image.load('data\\platforms\\flag_F.png'),
          'castle': pygame.image.load('data\\platforms\\castle.png')}


# платформы
class Platform(pygame.sprite.Sprite):
    def __init__(self, key, all_sprites, platforms, x, y):
        super().__init__(all_sprites, platforms)
        self.image = images[key]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# класс блока с вопросом, который дает 1000 очков
class SecretBlock(pygame.sprite.Sprite):
    def __init__(self, key, all_sprites, platforms, secret_blocks, x, y):
        super().__init__(all_sprites, platforms, secret_blocks)
        self.image = images[key]
        self.act_image = images['activated_sblock']
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    # если его активируют, то картинка меняется
    def change(self):
        self.image = self.act_image


# объект, который не является препятствием
class NotObstacle(pygame.sprite.Sprite):
    def __init__(self, key, all_sprites, x, y):
        super().__init__(all_sprites)
        self.image = images[key]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# объект замок, который является финишем уровня
class Castle(pygame.sprite.Sprite):
    def __init__(self, key, all_sprites, finish_group, x, y):
        super().__init__(all_sprites, finish_group)
        self.image = images[key]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# хотел сделать анимацию флага, но не получилось с ним договорится
# class Flag(pygame.sprite.Sprite):
#     def __init__(self, image, group1, group2, x, y, flag=False):
#         super().__init__(group1, group2)
#         self.image = image
#         self.rect = self.image.get_rect()
#         self.rect.x = x
#         self.rect.y = y
#         self.goDown = flag
#
#     def move(self, platforms):
#         self.rect = self.rect.move(0, 8)
#         if pygame.sprite.spritecollideany(self, platforms):
#             return False
#         return True
#
#     def update(self, player):
#         if pygame.sprite.spritecollideany(self, player):
#             return True
#         return False
