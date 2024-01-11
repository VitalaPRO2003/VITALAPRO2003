import pygame

move_speed = 3    # Константы: скорости,
jump_power = 10.5  # силы прыжка,
gravity = 0.35     # гравитации
anim_right = [pygame.image.load('data\\mario\\run1.png'),   # анимация бега вправо
              pygame.image.load('data\\mario\\run2.png'),
              pygame.image.load('data\\mario\\run3.png')]
anim_left = [pygame.image.load('data\\mario\\run1L.png'),   # анимация бега влево
             pygame.image.load('data\\mario\\run2L.png'),
             pygame.image.load('data\\mario\\run3L.png')]
anim_jump_left = pygame.image.load('data\\mario\\jumpL.png')  # прыжок влево
anim_jump_right = pygame.image.load('data\\mario\\jump.png')  # прыжок вправо
anim_stay_right = pygame.image.load('data\\mario\\stay.png')  # персонаж просто стоит смотрит вправо
anim_stay_left = pygame.image.load('data\\mario\\stayL.png')  # или влево
img_death = pygame.image.load('data\\mario\\death.png')   # анимация смерти персонажа
sounds = {'jump': 'data\\mario\\sounds\\jump.wav',    # звуки
          'death': 'data\\mario\\sounds\\death.wav',
          '1-up': 'data\\mario\\sounds\\1-up.wav'}


class Character(pygame.sprite.Sprite):
    def __init__(self, all_sprites, hero_group, x, y, timer):
        super().__init__(all_sprites, hero_group)
        self.vel_x = 0
        self.vel_y = 0
        self.image = anim_stay_right
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.cur_frame_left = 0
        self.cur_frame_right = 0
        self.FaceRight = True   # смотрит ли персонаж вправо
        self.lifes = 3       # количество жизней
        self.timer = timer   # таймер
        self.score = 0       # счетчик очков
        # первоначальное положение персонажа
        self.start_x = x
        self.start_y = y
        # стоит ли персонаж на земле?
        self.onGround = False   # всегда нет, т.к. нет проверки когда он на земле(

    def update(self, left, right, up, platforms_group, enemy_group, participles_group,
               secret_block_group, screen):
        # если прыгаем
        if up:
            if self.onGround:
                pygame.mixer.Sound(sounds['jump']).play()
                self.vel_y = -jump_power
                self.onGround = False
                if self.FaceRight:
                    self.image = anim_jump_right
                else:
                    self.image = anim_jump_left
            else:
                if self.FaceRight:
                    self.image = anim_jump_right
                else:
                    self.image = anim_jump_left
        else:
            if self.onGround:
                self.vel_y = 0
        # если идем влево
        if left:
            self.vel_x = -move_speed
            if self.onGround:
                self.cur_frame_left = (self.cur_frame_left + 1) % 3
                self.image = anim_left[self.cur_frame_left]
            self.FaceRight = False
        # если идем вправо
        if right:
            self.vel_x = move_speed
            if self.onGround:
                self.cur_frame_right = (self.cur_frame_right + 1) % 3
                self.image = anim_right[self.cur_frame_right]
            self.FaceRight = True
        # если не двигаемся, то стоим
        if not (left or right):
            self.vel_x = 0
            if self.FaceRight:
                self.image = anim_stay_right
            else:
                self.image = anim_stay_left
            self.cur_frame_left = 0
            self.cur_frame_right = 0
        # если не на земле, то поадаем
        if not self.onGround:
            self.vel_y += gravity
        # на самом деле персонаж всегда не на земле)
        self.onGround = False
        # выполняем движение по у
        self.rect = self.rect.move(0, self.vel_y)
        # если персонаж прыгет и пересекает коллайдер блока с вопросом, то
        if pygame.sprite.spritecollideany(self, secret_block_group):
            for sb in secret_block_group:
                if sb.rect.y < self.rect.y <= sb.rect.y + 32 and (sb.rect.x <= self.rect.x <= sb.rect.x + 32)\
                        and (sb.image != sb.act_image):
                    sb.change()
                    self.score += 1000
        # проверемя врезаемся ли мы в платформы
        self.collide(0, self.vel_y, platforms_group)
        # выполняем движение по х и проверям врезаемся ли мы в платформы
        self.rect = self.rect.move(self.vel_x, 0)
        self.collide(self.vel_x, 0, platforms_group)
        # проверяем пересечение с коллайдером врага
        if pygame.sprite.spritecollideany(self, enemy_group):
            if self.col_enemies(enemy_group, participles_group):
                self.death(screen)
        # если кол-во очков перевалило за 5000, то получаем +1 к жизням
        if self.score >= 5000:
            pygame.mixer.Sound(sounds['1-up']).play()
            self.score -= 5000
            self.lifes += 1
        # убывание таймера
        self.timer -= 0.01
        # если персонаж падает за экран, то он умирает
        if self.rect.y > 512:
            self.death(screen)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком

                if xvel > 0:  # если движется вправо
                    self.rect.right = p.rect.left  # то не движется вправо

                if xvel < 0:  # если движется влево
                    self.rect.left = p.rect.right  # то не движется влево

                if yvel > 0:  # если падает вниз
                    self.rect.bottom = p.rect.top  # то не падает вниз
                    self.onGround = True  # и становится на что-то твердое
                    self.vel_y = 0  # и энергия падения пропадает

                if yvel < 0 and ((p.rect.x < self.rect.x < p.rect.x + 32)
                                 or (p.rect.x < self.rect.x + self.rect.width < p.rect.x + 32)):  # если движется вверх
                                                                                        # и х попадает в ширину объекта
                    self.rect.top = p.rect.bottom  # то не движется вверх
                    self.vel_y = 0  # и энергия прыжка пропадает
                    self.onGround = False   # и начинаем падать

    # проверяем пересечение с врагом
    def col_enemies(self, enemies, participles_group):
        for enemy in enemies:
            if pygame.sprite.collide_rect(self, enemy):   # если пересечение есть
                # то проверяем персекает ли персонаж его сверху
                if (self.rect.y + self.rect.height >= enemy.rect.y) and (self.rect.y < enemy.rect.y):
                    pygame.mixer.Sound('data\\mario\\sounds\\bump.wav').play()
                    self.score += 500
                    enemy.death(participles_group)
                    return False   # если да, то умирает враг и прибавляются очки
                else:
                    return True   # если нет, то персонаж умирает

    # функции смерти персонажа
    def death(self, screen):
        self.image = img_death
        screen.blit(self.image, (512, 256))
        pygame.display.flip()
        self.lifes -= 1
        pygame.mixer.pause()
        pygame.mixer.Sound(sounds['death']).play()
        pygame.time.wait(int(pygame.mixer.Sound(sounds['death']).get_length() * 1000))
        pygame.mixer.unpause()
        # перемещение в начальные координаты уровня
        self.rect.x = self.start_x
        self.rect.y = self.start_y

    # нарисовка UI
    def draw_UI(self, screen):
        lst = [('Lives: ' + str(self.lifes), 100), ('Score: ' + str(self.score), 400),
               ('Time: ' + str(int(self.timer)), 700)]
        for i in lst:
            font = pygame.font.Font(None, 50)
            text = font.render(i[0], 1, (0, 0, 0))
            text_x = i[1]
            text_y = 20
            screen.blit(text, (text_x, text_y))

