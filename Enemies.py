import pygame
import random

move_speed = 1.5   # константы
gravity = 0.35
anim_walk = [pygame.image.load('data\\enemies\\Grib_1.png'),   # анимация ходьбы
             pygame.image.load('data\\enemies\\Grib_2.png')]


class Grib(pygame.sprite.Sprite):
    def __init__(self, all_sprites, enemies, x, y):
        super().__init__(all_sprites, enemies)
        self.all_sprites = all_sprites
        self.vel_x = move_speed
        self.vel_y = 0
        self.image = anim_walk[0]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.cur_frame = 0
        self.iter = 0
        self.onGround = False

    def update(self, platforms_group, enemy_group):
        # если не на земле, то падает
        if not self.onGround:
            self.vel_y += gravity
        self.onGround = False   # всегда падает
        self.iter += 1   # замедляем с помощью данной перменной анимация врага
        # выполняем перемещение по горизонтали и проверку пересечения с платформами
        self.rect = self.rect.move(self.vel_x, 0)
        self.collide(self.vel_x, 0, platforms_group)
        # делаем проверку на пересечение с себеподобными
        self.collide(self.vel_x, 0, enemy_group)
        # делаем перемещение по вертикали и проверяем персечение с платформами
        self.rect = self.rect.move(0, self.vel_y)
        self.collide(0, self.vel_y, platforms_group)
        # замедляем анимацию ходьбы в 10 раз
        if self.iter % 10 == 0:
            self.cur_frame = (self.cur_frame + 1) % 2
            self.image = anim_walk[self.cur_frame]
            self.iter = 0

    def collide(self, xvel, yvel, sprite_group):
        for p in sprite_group:
            if pygame.sprite.collide_rect(self, p) and (self != p):  # если есть пересечение объекта с игроком и
                                                                        # объект не является этим же объектом

                if xvel > 0:  # если движется вправо
                    self.rect.right = p.rect.left  # то не движется вправо
                    self.vel_x = -move_speed

                if xvel < 0:  # если движется влево
                    self.rect.left = p.rect.right  # то не движется влево
                    self.vel_x = move_speed

                if yvel > 0:  # если падает вниз
                    self.rect.bottom = p.rect.top  # то не падает вниз
                    self.onGround = True  # и становится на что-то твердое
                    self.vel_y = 0  # и энергия падения пропадает

    # крутая реализация смерти с кровью
    def death(self, participles_group):
        particle_count = 20
        numbers = range(-5, 6)
        for _ in range(particle_count):
            Particle(self.rect.topleft, random.choice(numbers),
                     random.choice(numbers), participles_group, self.all_sprites)
        self.kill()


# кровь
class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [pygame.Surface((5, 5))]
    fire[0].fill(pygame.Color('red'))
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy, participles_group, all_sprites):
        super().__init__(participles_group, all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = 0.35

    def update(self, screen_rect):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect((0, 0, screen_rect.width, screen_rect.height)):
            self.kill()
