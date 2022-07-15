import sys         # Модуль sys понадобится нам для закрытия игры
import os          # Модуль os нужен для работы с путями и файлами
import pygame      # Модуль pygame для реализации игровой логики
import random


pygame.mixer.pre_init(44100, -16, 1, 512)

# Инициализация модуля pygame
pygame.init()

# Параметры экрана размер и цвет
SCREEN_SIZE = (829, 600)
BG_COLOR = (0, 0, 0)
# Объект дисплея
screen = pygame.display.set_mode(SCREEN_SIZE, pygame.RESIZABLE)

# Фоновая картинка экрана
bg = pygame.image.load('images/garden.jpg').convert()

# Фоновая картинка и формат текста очков игры
score = pygame.image.load('images/score_fon.png').convert_alpha()
f = pygame.font.SysFont('arial', 30)

# Фоновый звук (загрузка, вкл. бесконечное повторение, громкость фонового звука)
pygame.mixer.music.load('sound/background.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.4)



class Game:
    def __init__(self, screen):
        self.screen = screen
        self.basket = Basket()
        self.apples = []
        self.game_score = 0

    # Функция обработки событий в игре (нажатия кнопок и т.д.)
    def handle_events(self, frame):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Нажатие на "Х" на окне программы.
                sys.exit()

        if frame % 150 == 0: # каждый 150-ый кадр
            new_apple = Apples()  # создается яблоко
            self.apples.append(new_apple) # добавляется в список объектов

    # Функция обработки столкновения яблок с корзинами
    def check_collisions(self):
        apples_rects = [] # список хитбоксов всех яблок
        point = []  # список очков для яблок
        for appl in self.apples:
            apples_rects.append(appl.rect)
            point.append(appl.score)

        # Столкновение яблок с корзинами
        # Индекс яблока, столкнувшегося с корзиной
        hit = self.basket.rect.collidelist(apples_rects)
        if hit != -1:  # если есть столкновение
            self.basket.music.play()  # проигрывается звук стокновения
            self.game_score += point[hit] # подсчет очков при стокновении яблока с корзиной
            del self.apples[hit]  # ...удалить яблоко из списка

    # Функция обработки нажатий клавиш влево, вправо
    def move_objects(self, objects_list):
        for objects in objects_list:
            for obj in objects:
                if obj == self.basket:
                    bt = pygame.key.get_pressed()
                    if bt[pygame.K_LEFT]:
                        obj.move_left()
                    elif bt[pygame.K_RIGHT]:
                        obj.move_right()
                else:
                    obj.move()

    # Функция отрислвки всех объектов в игре
    def draw(self, objects_list, debug=False):
        # Закрашиваем экран после нажатия кнопки движения
        self.screen.fill(BG_COLOR)

        # Картинка на фон
        screen.blit(bg, (0, 0))

        # Отображаем картинку очков, формат текста очков, отражение очков на экране
        screen.blit(score, (0, 0))
        score_text = f.render(str(self.game_score), 1, (94, 138, 14))
        screen.blit(score_text, (35, 10))

        # Берем элемент из списка и производим его отрисовку на поле
        for objects in objects_list:
            for obj in objects:
                self.screen.blit(obj.image, obj.rect)

        # Дебаг режим, отрисовываем хитбокс
        if debug:
            for objects in objects_list:
                for obj in objects:
                    pygame.draw.rect(self.screen, (0, 255, 0), obj.rect, 2)

        # Обновляем изображение на экране
        pygame.display.update()


    # Главный цикл программы. Вызывается 1 раз за игру
    def run(self):
        clock = pygame.time.Clock()
        frame = 0
        # Игровой цикл (главный цикл), передаем сюда все объекты, которые есть в игре
        while True:
            clock.tick(60)
            self.handle_events(frame)
            self.check_collisions()
            self.move_objects([[self.basket], self.apples])
            self.draw([[self.basket], self.apples], debug=False)
            frame += 1



class Basket:
    def __init__(self):
        # Положение корзины на старте
        self.pos_x = SCREEN_SIZE[0]//2
        self.pos_y = SCREEN_SIZE[1] - 15
        # Загрузка картинки корзины
        self.image = pygame.image.load(os.path.join("images", "basket2.png"))
        # Получаем размеры (хитбокс) картинки
        self.rect = self.image.get_rect(centerx=self.pos_x, bottom=self.pos_y)
        self.speed = 5
        self.music = pygame.mixer.Sound('sound/pik_3.wav')
    # Движение корзины влево при нажатии стерки <-
    def move_left(self):
        self.pos_x -= self.speed
        if self.pos_x <= 70:
            self.pos_x = 70

        self.rect = self.image.get_rect(centerx=self.pos_x, bottom=self.pos_y)

    # Движение корзины вправо при нажатии стерки ->
    def move_right(self):
        self.pos_x += self.speed
        if self.pos_x >= SCREEN_SIZE[0]-70:
            self.pos_x = SCREEN_SIZE[0]-70

        self.rect = self.image.get_rect(centerx=self.pos_x, bottom=self.pos_y)

class Apples:
    def __init__(self):
        # Список вариаций яблок
        data = [{'path': 'green_2.png', 'score': 100, 'speed': 1}, {'path': 'yellow_2.png', 'score': 150, 'speed': 2},
                {'path': 'red_2.png', 'score': 200, 'speed': 3}]
        # Выбор случайного индекса
        self.idx = random.randint(0, len(data)-1)
        # Формирование случайного яблока с соотвествующими параметрами (на основе случайного индекса)
        self.image = pygame.image.load("images/"+str(data[self.idx]['path'])).convert_alpha()
        self.score = data[self.idx]['score']
        self.speed = data[self.idx]['speed']
        # Появление яблока на экране
        self.pos_x = random.randint(40, SCREEN_SIZE[0]-40)
        self.pos_y = -40
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))
        self.music = pygame.mixer.Sound('sound/bah_2.wav')


    # Отрисовка падения яблок
    def move(self):
        self.check_borders()  # Обработка выхода за границы
        self.pos_y += self.speed # Падение яблока, перемещение по оси Y
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))

    # Обработка выхода за нижнюю границу экрана
    def check_borders(self):
        # Если центр яблока за нижней границей...
        if self.pos_y > (SCREEN_SIZE[1]): #
            self.music.play() # ... проигрывается звук столкновения
            self.pos_y = -40  # ...перемещаем его за верхнюю границу
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))

game = Game(screen)
game.run()
