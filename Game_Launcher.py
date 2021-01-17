import os
import random
import sys

import pygame

# подготовка
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
size = width, height = 1280, 720
screen = pygame.display.set_mode(size)
screen2 = pygame.Surface(screen.get_size())
clock = pygame.time.Clock()
FPS = 15
# ивент для таймера
time = 0
MYEVENTTYPE = pygame.USEREVENT + 1
pygame.time.set_timer(MYEVENTTYPE, 1000)
pygame.display.set_caption('Game Launcher')
pygame.display.set_icon(pygame.image.load('data/game.ico'))
# музыка
click_sound = pygame.mixer.Sound("data/Music/click.wav")
click_sound.set_volume(0.5)
victory_sound = pygame.mixer.Sound("data/Music/vicrory.wav")
victory_sound.set_volume(0.5)
death_sound = pygame.mixer.Sound('data/Music/death.wav')
death_sound.set_volume(0.5)
pygame.mixer.music.set_volume(0.25)
menu_music = "data/Music/menu.mp3"
zmeika_music = "data/Music/game.mp3"
maze_music = "data/Music/game2.mp3"
shashki_music = "data/Music/game(GAYM)4.mp3"

# основной персонаж для лабиринта
player = None

# флаги
start_flag = True
menu_flag = False
zmeika_flag = False
zmeika_flag_2 = True
zmeika_apple_flag = False
zmeika_death_flag = False
zmeika_pause_flag = False
shashki_flag = False
maze_flag = False
maze_level_1 = False
maze_level_2 = False
maze_level_3 = False
maze_pause_flag = False

# группы спрайтов
sprites_start = pygame.sprite.Group()
sprites_menu = pygame.sprite.Group()
sprites_zmeika = pygame.sprite.Group()
sprites_zmeika_2 = pygame.sprite.Group()
sprites_zmeika_3 = pygame.sprite.Group()
sprites_zmeika_4 = pygame.sprite.Group()
sprites_maze = pygame.sprite.Group()
sprites_maze_2 = pygame.sprite.Group()
sprites_maze_3 = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()

# переменные для проверки
color_1 = True
color_2 = True
color_3 = True
color_4 = True
color_5 = True
color_6 = True
color_7 = True
color_8 = True
color_9 = True
color_10 = True
color_11 = True
color_12 = True


# данные для игры змейка
def data_zmeika():
    with open("data/zmeika.txt", encoding="utf8") as f:
        training_zmeika = f.readline().split('\n')[0][10:]
        record_zmeika = int(f.readline().split('\n')[0][8:])
    return training_zmeika, record_zmeika


training_zmeika, record_zmeika = data_zmeika()
direction_zmeika = 'left'
schet = 0
finish = []


# функция для очистки данных о змейке
def clear_zmeika():
    with open("data/zmeika.txt", mode='w', encoding='utf-8') as f:
        f.writelines(f'Обучение: не пройдено')
        f.writelines('\n')
        f.writelines(f'Рекорд: 0')


# функция для очистки данных о лабиринте
def clear_maze(level):
    global level_1_maze, level_2_maze, level_3_maze, training_maze, level_1_maze, level_2_maze, level_3_maze
    if level == 1:
        with open("data/maze.txt", mode='w', encoding='utf-8') as f:
            f.writelines(f'Обучение: {training_maze}')
            f.writelines('\n')
            f.writelines(f'1 уровень: не пройден - 0с')
            f.writelines('\n')
            f.writelines(f'2 уровень: {level_2_maze[0]} - {level_2_maze[1]}')
            f.writelines('\n')
            f.writelines(f'3 уровень: {level_3_maze[0]} - {level_3_maze[1]}')
    elif level == 2:
        with open("data/maze.txt", mode='w', encoding='utf-8') as f:
            f.writelines(f'Обучение: {training_maze}')
            f.writelines('\n')
            f.writelines(f'1 уровень: {level_1_maze[0]} - {level_1_maze[1]}')
            f.writelines('\n')
            f.writelines(f'2 уровень: не пройден - 0с')
            f.writelines('\n')
            f.writelines(f'3 уровень: {level_3_maze[0]} - {level_3_maze[1]}')
    elif level == 3:
        with open("data/maze.txt", mode='w', encoding='utf-8') as f:
            f.writelines(f'Обучение: {training_maze}')
            f.writelines('\n')
            f.writelines(f'1 уровень: {level_1_maze[0]} - {level_1_maze[1]}')
            f.writelines('\n')
            f.writelines(f'2 уровень: {level_2_maze[0]} - {level_2_maze[1]}')
            f.writelines('\n')
            f.writelines(f'3 уровень: не пройден - 0с')
    elif level == 'x':
        with open("data/maze.txt", mode='w', encoding='utf-8') as f:
            f.writelines(f'Обучение: не пройдено')
            f.writelines('\n')
            f.writelines(f'1 уровень: {level_1_maze[0]} - {level_1_maze[1]}')
            f.writelines('\n')
            f.writelines(f'2 уровень: {level_2_maze[0]} - {level_2_maze[1]}')
            f.writelines('\n')
            f.writelines(f'3 уровень: {level_3_maze[0]} - {level_3_maze[1]}')
    training_maze, level_1_maze, level_2_maze, level_3_maze = data_maze()


# данные для игры лабиринт
def data_maze():
    with open("data/maze.txt", encoding='utf8') as f:
        training_maze = f.readline().split('\n')[0][10:]
        level_1_maze = f.readline().split('\n')[0][11:].split(' - ')
        level_2_maze = f.readline().split('\n')[0][11:].split(' - ')
        level_3_maze = f.readline().split('\n')[0][11:].split(' - ')
    return training_maze, level_1_maze, level_2_maze, level_3_maze


training_maze, level_1_maze, level_2_maze, level_3_maze = data_maze()
step = 20
tile_width = tile_height = 20


# функция для открытия фотографий
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# функция для отображения информации на экране для змейки
def zmeika_text(event):
    global schet, record_zmeika
    training_zmeika, record_zmeika = data_zmeika()
    if event == 'game':
        intro_text = [f'Очки: {schet}',
                      f'Рекорд: {record_zmeika}']
        font = pygame.font.Font(None, 60)
        text_coord = 15

        # вывод текста на экран
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('#444244'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 15
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
    elif event == 'pause':
        propysk = '                    '
        intro_text = [f'                  Пауза',
                      f'{propysk}     Вы можете:',
                      f'Вернуться в главное меню',
                      f'(счет не будет сохранен)',
                      f'Начать заново',
                      f'Продолжить']
        font = pygame.font.Font(None, 90)
        text_coord = 20

        # вывод текста на экран
        for line in range(len(intro_text)):
            string_rendered = font.render(intro_text[line], 1, pygame.Color('#444244'))
            intro_rect = string_rendered.get_rect()
            if line < 2:
                text_coord += 5
                intro_rect.x = 250
            elif line == 2:
                text_coord += 40
                intro_rect.x = 265
            elif line == 3:
                text_coord += 5
                intro_rect.x = 265
            else:
                text_coord += 67
                intro_rect.x = 265
            intro_rect.top = text_coord
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
            font = pygame.font.Font(None, 60)
    elif event == 'death':
        propysk = '                    '
        intro_text = [f'                  Вы проиграли',
                      f'Ваш результат: {str(schet)}',
                      f'Ваш рекорд: {str(record_zmeika)}',
                      f'Вы можете:',
                      f'Вернуться в главное меню',
                      f'Начать заново']
        font = pygame.font.Font(None, 80)
        text_coord = 15

        # вывод текста на экран
        for line in range(len(intro_text)):
            string_rendered = font.render(intro_text[line], 1, pygame.Color('#444244'))
            intro_rect = string_rendered.get_rect()
            if line == 0:
                text_coord += 5
                intro_rect.x = 180
            elif line < 3:
                text_coord += 5
                intro_rect.x = 451
            elif line == 3:
                text_coord += 5
                intro_rect.x = 450
            elif line == 4:
                text_coord += 30
                intro_rect.x = 265
            else:
                text_coord += 80
                intro_rect.x = 265
            intro_rect.top = text_coord
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
            font = pygame.font.Font(None, 60)


# функция для отображения информации на экране для лабиринта
def maze_text(event, time=None):
    global level_1_maze, level_2_maze, level_3_maze
    training_maze, level_1_maze, level_2_maze, level_3_maze = data_maze()
    if event == 'game':
        propysk = '                    '
        intro_text = [f'Выберите уровень',
                      f'{propysk}{propysk}Результат                         Время',
                      f'1 уровень:{propysk}{level_1_maze[0]}{propysk}        {level_1_maze[1]}',
                      f'2 уровень:{propysk}{level_2_maze[0]}{propysk}        {level_2_maze[1]}',
                      f'3 уровень:{propysk}{level_3_maze[0]}{propysk}        {level_3_maze[1]}']
        font = pygame.font.Font(None, 90)
        text_coord = 15

        # вывод текста на экран
        for line in range(len(intro_text)):
            string_rendered = font.render(intro_text[line], 1, pygame.Color('#444244'))
            intro_rect = string_rendered.get_rect()
            if line == 0:
                text_coord += 5
                intro_rect.x = 350
            elif line == 1:
                text_coord += 390
                intro_rect.x = 15
            elif line > 1:
                text_coord += 25
                intro_rect.x = 15
            intro_rect.top = text_coord
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
            font = pygame.font.Font(None, 50)
    elif event == 'pause':
        propysk = '                    '
        intro_text = [f'                  Пауза',
                      f'{propysk}     Вы можете:',
                      f'Вернуться в главное меню',
                      f'(время не сохраниться)',
                      f'Начать заново',
                      f'Продолжить']
        font = pygame.font.Font(None, 90)
        text_coord = 20

        # вывод текста на экран
        for line in range(len(intro_text)):
            string_rendered = font.render(intro_text[line], 1, pygame.Color('#444244'))
            intro_rect = string_rendered.get_rect()
            if line < 2:
                text_coord += 5
                intro_rect.x = 250
            elif line == 2:
                text_coord += 40
                intro_rect.x = 265
            elif line == 3:
                text_coord += 5
                intro_rect.x = 265
            else:
                text_coord += 67
                intro_rect.x = 265
            intro_rect.top = text_coord
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
            font = pygame.font.Font(None, 60)
    elif event == 'level':
        intro_text = ['']
        if maze_level_1:
            intro_text = [f'Время: {time}с',
                          f'Лучшее: {level_1_maze[1]}']
        elif maze_level_2:
            intro_text = [f'Время: {time}с',
                          f'Лучшее: {level_2_maze[1]}']
        elif maze_level_3:
            intro_text = [f'Время: {time}с',
                          f'Лучшее: {level_3_maze[1]}']
        font = pygame.font.Font(None, 60)
        text_coord = 15

        # вывод текста на экран
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('#444244'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 15
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)


# функция для закрытия приложения
def terminate():
    pygame.quit()
    sys.exit()


# функция для занесения рекорда змейки
def zmeika_record():
    global record_zmeika, schet, training_zmeika
    death_sound.play()
    if schet <= record_zmeika:
        pass
    else:
        with open("data/zmeika.txt", mode='w', encoding='utf-8') as f:
            f.writelines(f'Обучение: {training_zmeika}')
            f.writelines('\n')
            f.writelines(f'Рекорд: {schet}')
        training_zmeika, record_zmeika = data_zmeika()
    clock.tick(10)


# функция для занесения рекорда лабиринта
def maze_record(time, level):
    global training_maze, level_1_maze, level_2_maze, level_3_maze, maze_pause_flag, maze_level_1, maze_level_2, \
        maze_level_3
    victory_sound.play()
    if level == 1:
        if (level_1_maze[0] == 'не пройден') or (level_1_maze[0] == 'пройден' and time <= int(level_1_maze[1][:-1])):
            with open("data/maze.txt", mode='w', encoding='utf-8') as f:
                f.writelines(f'Обучение: пройдено')
                f.writelines('\n')
                f.writelines(f'1 уровень: пройден - {time}с')
                f.writelines('\n')
                f.writelines(f'2 уровень: {level_2_maze[0]} - {level_2_maze[1]}')
                f.writelines('\n')
                f.writelines(f'3 уровень: {level_3_maze[0]} - {level_3_maze[1]}')
        elif level_1_maze[0] == 'пройден' and time > int(level_1_maze[1][:-1]):
            pass
        maze_pause_flag = False
        maze_level_1 = False
    elif level == 2:
        if (level_2_maze[0] == 'не пройден') or (level_2_maze[0] == 'пройден' and time <= int(level_2_maze[1][:-1])):
            with open("data/maze.txt", mode='w', encoding='utf-8') as f:
                f.writelines(f'Обучение: пройдено')
                f.writelines('\n')
                f.writelines(f'1 уровень: {level_1_maze[0]} - {level_1_maze[1]}')
                f.writelines('\n')
                f.writelines(f'2 уровень: пройден - {time}с')
                f.writelines('\n')
                f.writelines(f'3 уровень: {level_3_maze[0]} - {level_3_maze[1]}')
        elif level_2_maze[0] == 'пройден' and time > int(level_2_maze[1][:-1]):
            pass
        maze_pause_flag = False
        maze_level_2 = False
    elif level == 3:
        if (level_3_maze[0] == 'не пройден') or (level_3_maze[0] == 'пройден' and time <= int(level_3_maze[1][:-1])):
            with open("data/maze.txt", mode='w', encoding='utf-8') as f:
                f.writelines(f'Обучение: пройдено')
                f.writelines('\n')
                f.writelines(f'1 уровень: {level_1_maze[0]} - {level_1_maze[1]}')
                f.writelines('\n')
                f.writelines(f'2 уровень: {level_2_maze[0]} - {level_2_maze[1]}')
                f.writelines('\n')
                f.writelines(f'3 уровень: пройден - {time}с')
        elif level_3_maze[0] == 'пройден' and time > int(level_3_maze[1][:-1]):
            pass
        maze_pause_flag = False
        maze_level_3 = False
    clock.tick(10)


# класс кнопки для начала
class btn_next(pygame.sprite.Sprite):
    image = load_image("button-right.jpg")
    image2 = load_image("button-right2.jpg")

    def __init__(self, *group):
        super().__init__(*group)
        self.rect = self.image.get_rect()
        self.rect.x = (width // 2) - self.image.get_size()[0] // 2
        self.rect.y = (height // 2)
        self.color = True

    def update(self, *args):
        global start_flag, menu_flag, color_1
        if color_1:
            self.image = btn_next.image
        else:
            self.image = btn_next.image2
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            click_sound.play()
            clock.tick(10)
            start_flag = False
            menu_flag = True
            clock.tick(5)
            menu_screen()


# класс кнопки для запуска игры змейка
class btn_zmeika(pygame.sprite.Sprite):
    image = load_image("ZMEIKA.jpg")
    image2 = load_image("ZMEIKA2.jpg")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = btn_zmeika.image
        self.rect = self.image.get_rect()
        self.rect.x = 170
        self.rect.y = (height // 2) + 75

    def update(self, *args):
        global menu_flag, zmeika_flag, color_2
        if color_2:
            self.image = btn_zmeika.image
        else:
            self.image = btn_zmeika.image2
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            click_sound.play()
            clock.tick(10)
            menu_flag = False
            zmeika_flag = True
            pygame.mixer.music.load(zmeika_music)
            pygame.mixer.music.play(-1, 0.0, 1500)
            zmeika()


# класс стрелки для указания направления в змейке
class zmeika_arrow(pygame.sprite.Sprite):
    image = load_image("strelka_left.png")
    image2 = load_image("strelka_right.png")
    image3 = load_image("strelka_up.png")
    image4 = load_image("strelka_down.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = zmeika_arrow.image
        self.rect = self.image.get_rect()
        self.rect.x = 1060
        self.rect.y = (height // 2) + 50

    def update(self, dop=None, *args):
        if args and args[0].type == pygame.KEYDOWN and dop:
            if dop == 'left':
                self.image = zmeika_arrow.image
            elif dop == 'right':
                self.image = zmeika_arrow.image2
            elif dop == 'up':
                self.image = zmeika_arrow.image3
            elif dop == 'down':
                self.image = zmeika_arrow.image4


# класс кнопки для очистки рекорда и повтора обучения в змейке
class CClear(pygame.sprite.Sprite):
    image = load_image("clear.jpg")
    image2 = load_image("clear2.jpg")

    def __init__(self, *group, x=15, y=130, game):
        super().__init__(*group)
        self.image = CClear.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.game = game

    def update(self, *args):
        global color_5, maze_level_1, maze_level_2, maze_level_3
        if color_5:
            self.image = CClear.image
        else:
            self.image = CClear.image2
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            click_sound.play()
            clock.tick(10)
            if self.game == 'zmeika':
                clear_zmeika()
            if self.game == 'level':
                if maze_level_1:
                    clear_maze(1)
                elif maze_level_2:
                    clear_maze(2)
                elif maze_level_3:
                    clear_maze(3)
            if self.game == 'maze':
                clear_maze('x')


# класс кнопки продолжение после паузы
class Continues(pygame.sprite.Sprite):
    image = load_image("button-right.jpg")
    image2 = load_image("button-right2.jpg")

    def __init__(self, *group, x, y, game):
        super().__init__(*group)
        self.image = Continues.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.game = game

    def update(self, *args):
        global color_9, zmeika_pause_flag, zmeika_flag_2, maze_pause_flag
        if color_9:
            self.image = Continues.image
        else:
            self.image = Continues.image2
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            click_sound.play()
            clock.tick(10)
            if self.game == 'zmeika':
                zmeika_pause_flag = False
                zmeika_flag_2 = True
            if self.game == 'maze':
                maze_pause_flag = False


# класс кнопки для возвращения в меню
class Back(pygame.sprite.Sprite):
    image = load_image("Backward.jpg")
    image2 = load_image("Backward2.jpg")

    def __init__(self, *group, x, y, game):
        super().__init__(*group)
        self.image = Back.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.game = game

    def update(self, *args):
        global color_7, menu_flag, zmeika_flag, maze_flag, maze_level_1, maze_level_2, maze_level_3, maze_pause_flag
        if color_7:
            self.image = Back.image
        else:
            self.image = Back.image2
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            click_sound.play()
            clock.tick(10)
            if self.game == 'zmeika':
                menu_flag = True
                zmeika_flag = False
                pygame.mixer.music.load(menu_music)
                pygame.mixer.music.play(-1, 0.0, 1500)
                menu_screen()
            if self.game == 'maze':
                menu_flag = True
                maze_flag = False
                pygame.mixer.music.load(menu_music)
                pygame.mixer.music.play(-1, 0.0, 1500)
                menu_screen()
            if self.game == 'level':
                maze_pause_flag = False
                maze_level_1 = False
                maze_level_2 = False
                maze_level_3 = False


# класс кнопки для рестарта
class Reset(pygame.sprite.Sprite):
    image = load_image("reset.jpg")
    image2 = load_image("reset2.jpg")

    def __init__(self, *group, x, y, game):
        super().__init__(*group)
        self.image = Reset.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.game = game

    def update(self, *args, level=None):
        global color_8, player_group, time, tiles_group, walls_group, player, maze_pause_flag
        if color_8:
            self.image = Reset.image
        else:
            self.image = Reset.image2
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            click_sound.play()
            clock.tick(10)
            if self.game == 'zmeika':
                zmeika()
            if self.game == 'maze':
                tiles_group = pygame.sprite.Group()
                player_group = pygame.sprite.Group()
                walls_group = pygame.sprite.Group()
                time = 0
                maze_pause_flag = False
                player = None
                player, level_x, level_y = generate_level(load_level('level1.txt'))


# класс кнопки для паузы
class Pause(pygame.sprite.Sprite):
    image = load_image("pause.jpg")
    image2 = load_image("pause2.jpg")

    def __init__(self, *group, x, y, game):
        super().__init__(*group)
        self.image = Pause.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.game = game

    def update(self, *args):
        global color_6, zmeika_pause_flag, zmeika_flag_2, maze_pause_flag
        if color_6:
            self.image = Pause.image
        else:
            self.image = Pause.image2
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            click_sound.play()
            clock.tick(10)
            if self.game == 'zmeika':
                zmeika_pause_flag = True
                zmeika_flag_2 = False
            if self.game == 'maze':
                maze_pause_flag = True


# класс кнопки для запуска игры шашки
class btn_shashki(pygame.sprite.Sprite):
    image = load_image("shashki.jpg")
    image2 = load_image("shashki2.jpg")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = btn_shashki.image
        self.rect = self.image.get_rect()
        self.rect.x = 540
        self.rect.y = (height // 2) + 75

    def update(self, *args):
        global menu_flag, shashki_flag, color_3
        if color_3:
            self.image = btn_shashki.image
        else:
            self.image = btn_shashki.image2
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            click_sound.play()
            clock.tick(10)
            menu_flag = False
            shashki_flag = True
            shashki()


# класс кнопки для запуска игры лабиринт
class btn_maze(pygame.sprite.Sprite):
    image = load_image("maze.jpg")
    image2 = load_image("maze2.jpg")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = btn_maze.image
        self.rect = self.image.get_rect()
        self.rect.x = 910
        self.rect.y = (height // 2) + 75

    def update(self, *args):
        global menu_flag, maze_flag, color_4
        if color_4:
            self.image = btn_maze.image
        else:
            self.image = btn_maze.image2
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            click_sound.play()
            clock.tick(10)
            menu_flag = False
            maze_flag = True
            pygame.mixer.music.load(maze_music)
            pygame.mixer.music.play(-1, 0.0, 1500)
            maze()


# класс кнопки для выбора уровня в лабиринте
class btn_level_maze(pygame.sprite.Sprite):
    def __init__(self, *group, level):
        super().__init__(*group)
        self.level = level
        if self.level == 1:
            self.image = load_image("level11.jpg")
            self.rect = self.image.get_rect()
            self.rect.x = 170
            self.rect.y = (height // 2)
        elif self.level == 2:
            self.image = load_image("level21.jpg")
            self.rect = self.image.get_rect()
            self.rect.x = 540
            self.rect.y = (height // 2)
        elif self.level == 3:
            self.image = load_image("level31.jpg")
            self.rect = self.image.get_rect()
            self.rect.x = 910
            self.rect.y = (height // 2)

    def update(self, *args):
        global maze_level_1, maze_level_2, maze_level_3, color_10, color_11, color_12
        if self.level == 1:
            if color_10:
                self.image = load_image("level11.jpg")
            else:
                self.image = load_image("level12.jpg")
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                    self.rect.collidepoint(args[0].pos):
                click_sound.play()
                clock.tick(10)
                maze_level_1 = True
        elif self.level == 2:
            if color_11:
                self.image = load_image("level21.jpg")
            else:
                self.image = load_image("level22.jpg")
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                    self.rect.collidepoint(args[0].pos):
                click_sound.play()
                clock.tick(10)
                maze_level_2 = True
        elif self.level == 3:
            if color_12:
                self.image = load_image("level31.jpg")
            else:
                self.image = load_image("level32.jpg")
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                    self.rect.collidepoint(args[0].pos):
                click_sound.play()
                clock.tick(10)
                maze_level_3 = True


# картинка уровня для лабиринта
class map_level_maze(pygame.sprite.Sprite):
    def __init__(self, *group, level):
        super().__init__(*group)
        self.level = level
        if self.level == 1:
            self.image = load_image("map1.jpg")
            self.rect = self.image.get_rect()
            self.rect.x = 170
            self.rect.y = (height // 2) - 200
        elif self.level == 2:
            self.image = load_image("map2.jpg")
            self.rect = self.image.get_rect()
            self.rect.x = 540
            self.rect.y = (height // 2) - 200
        elif self.level == 3:
            self.image = load_image("map3.jpg")
            self.rect = self.image.get_rect()
            self.rect.x = 910
            self.rect.y = (height // 2) - 200

    def update(self, *args):
        pass


# начальное окно
def start_screen():
    global start_flag, color_1
    pygame.mixer.music.load(menu_music)
    pygame.mixer.music.play(-1, 0.0, 1500)
    fon = pygame.transform.scale(load_image('bg_start.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    # текст на экране
    spisok_nomera = [random.randint(0, 9) for i in range(7)]
    nomer = f'+7({random.choice([495, 902, 906, 909, 910, 916, 964, 968, 977])}){spisok_nomera[0]}{spisok_nomera[1]}{spisok_nomera[2]}-' \
            f'{spisok_nomera[3]}{spisok_nomera[4]}-{spisok_nomera[5]}{spisok_nomera[6]}'
    propysk = '                                        '
    intro_text = [
        f'program by SANYA_TEAM{propysk}{propysk}{propysk}{propysk}{propysk}  Здесь могла быть ваша реклама:',
        f'on pygame{propysk}{propysk}{propysk}{propysk}{propysk}                               {nomer}']
    font = pygame.font.Font(None, 23)
    text_coord = 655

    # вывод текста на экран
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('#444244'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 15
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    # игровой цикл
    btn_next(sprites_start)
    while start_flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                sprites_start.update(event)
            elif event.type == pygame.MOUSEMOTION:
                if ((width // 2) - 50) < event.pos[0] < (((width // 2) - 50) + 100) and \
                        (height // 2) < event.pos[1] < ((height // 2) + 100):
                    color_1 = False
                else:
                    color_1 = True
                sprites_start.update(event)
        sprites_start.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


# окно меню
def menu_screen():
    global menu_flag, color_2, color_3, color_4
    fon = pygame.transform.scale(load_image('bg_menu.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    pygame.display.set_caption('Game Launcher')
    pygame.display.set_icon(pygame.image.load('data/game.ico'))
    # текст на экране
    font = pygame.font.Font(None, 75)
    text_coord = 110
    propysk = '                  '
    intro_text = [f'{propysk}ВЫБЕРИТЕ ИГРУ',
                  f'     Змейка{propysk}               Шашки{propysk}             Лабиринт']
    # вывод текста на экран
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('#444244'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = text_coord
        text_coord += 235
        intro_rect.x = 170
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        font = pygame.font.Font(None, 44)

    # игровой цикл
    btn_zmeika(sprites_menu)
    btn_shashki(sprites_menu)
    btn_maze(sprites_menu)
    while menu_flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                sprites_menu.update(event)
            elif event.type == pygame.MOUSEMOTION:
                if 170 < event.pos[0] < (170 + 200) and \
                        (height // 2) + 75 < event.pos[1] < ((height // 2) + 75 + 200):
                    color_2 = False
                else:
                    color_2 = True
                if 540 < event.pos[0] < (540 + 200) and \
                        (height // 2) + 75 < event.pos[1] < ((height // 2) + 75 + 200):
                    color_3 = False
                else:
                    color_3 = True
                if 910 < event.pos[0] < (910 + 200) and \
                        (height // 2) + 75 < event.pos[1] < ((height // 2) + 75 + 200):
                    color_4 = False
                else:
                    color_4 = True
                sprites_menu.update(event)
        sprites_menu.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


# доска для змейки
class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # значения по умолчанию
        self.left = 300
        self.top = 28
        self.cell_size = 35
        self.dlina = 4
        self.board = [[0] * width for _ in range(height)]
        self.zmeya = {1: [9, 9], 2: [10, 9], 3: [11, 9], 4: [12, 9]}
        self.apple_coord = []

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    # наносит змею на поле
    def zmeia(self):
        self.board = [[0] * width for _ in range(height)]
        for i in range(1, self.dlina + 1):
            self.board[self.zmeya[i][1]][self.zmeya[i][0]] = 1

    # отрисовка
    def render(self):
        global zmeika_flag_2
        clock.tick(10)
        if zmeika_flag_2:
            colors = [(0, 0, 0), pygame.Color('#349852'), (255, 0, 0)]
            self.zmeia()
            self.apple()
            for y in range(self.height):
                for x in range(self.width):
                    if self.board[y][x] == 0 or self.board[y][x] == 2:
                        pygame.draw.rect(screen, colors[self.board[y][x]],
                                         (x * self.cell_size + self.left, y * self.cell_size + self.top,
                                          self.cell_size, self.cell_size))
                    elif self.board[y][x] == 1:
                        pygame.draw.rect(screen, colors[self.board[y][x]],
                                         (x * self.cell_size + self.left, y * self.cell_size + self.top,
                                          self.cell_size, self.cell_size))
                        pygame.draw.rect(screen, (0, 0, 0),
                                         (x * self.cell_size + self.left, y * self.cell_size + self.top,
                                          self.cell_size, self.cell_size), 1)
                        if [x, y] == self.zmeya[1]:
                            pygame.draw.polygon(screen, pygame.Color('#a2e59b'),
                                                [(self.left + self.cell_size * x + 17,
                                                  self.top + self.cell_size * y + 8),
                                                 (self.left + self.cell_size * x + 27,
                                                  self.top + self.cell_size * y + 17),
                                                 (self.left + self.cell_size * x + 17,
                                                  self.top + self.cell_size * y + 27),
                                                 (self.left + self.cell_size * x + 8,
                                                  self.top + self.cell_size * y + 17)])

    # рисуем яблоко
    def apple(self):
        global zmeika_apple_flag
        if not zmeika_apple_flag:
            while not zmeika_apple_flag:
                x = random.randint(0, 18)
                y = random.randint(0, 18)
                if [x, y] in [self.zmeya[i] for i in range(1, self.dlina + 1)]:
                    continue
                else:
                    self.apple_coord = [x, y]
                    zmeika_apple_flag = True
        if self.apple_coord:
            self.board[self.apple_coord[1]][self.apple_coord[0]] = 2

    # проверка на то что съели
    def check_apple(self, new):
        global zmeika_apple_flag, schet, FPS
        if self.apple_coord == self.zmeya[1].copy():
            zmeika_apple_flag = False
            schet += 50
            FPS += 1
            self.dlina += 1
            self.zmeya[self.dlina] = new
            self.render()

    # проверка на смену направления
    def check(self, curent, new):
        global direction_zmeika
        if curent == new:
            pass
        else:
            if (curent == 'up' and new == 'down') or (curent == 'down' and new == 'up') or \
                    (curent == 'left' and new == 'right') or (curent == 'right' and new == 'left'):
                pass
            else:
                direction_zmeika = new
                return True

    # передвижение змейки
    def crawl(self, direction):
        new_last = self.zmeya[self.dlina].copy()
        if direction == 'left':
            curent = self.zmeya[1].copy()
            curent[0] -= 1
            for i in range(self.dlina, 0, -1):
                if i == 1:
                    self.zmeya[i] = curent
                else:
                    self.zmeya[i] = self.zmeya[i - 1]
        elif direction == 'right':
            curent = self.zmeya[1].copy()
            curent[0] += 1
            for i in range(self.dlina, 0, -1):
                if i == 1:
                    self.zmeya[i] = curent
                else:
                    self.zmeya[i] = self.zmeya[i - 1]
        elif direction == 'up':
            curent = self.zmeya[1].copy()
            curent[1] -= 1
            for i in range(self.dlina, 0, -1):
                if i == 1:
                    self.zmeya[i] = curent
                else:
                    self.zmeya[i] = self.zmeya[i - 1]
        elif direction == 'down':
            curent = self.zmeya[1].copy()
            curent[1] += 1
            for i in range(self.dlina, 0, -1):
                if i == 1:
                    self.zmeya[i] = curent
                else:
                    self.zmeya[i] = self.zmeya[i - 1]
        self.check_apple(new_last)
        self.death()

    # проверка смерти
    def death(self):
        global zmeika_flag_2, zmeika_death_flag
        curent = self.zmeya[1].copy()
        if (curent[0] < 0 or curent[0] > 18) or \
                (curent[1] < 0 or curent[1] > 18) or \
                curent in [self.zmeya[i] for i in range(2, self.dlina + 1)]:
            zmeika_record()
            zmeika_flag_2 = False
            zmeika_death_flag = True


# окно змейки
def zmeika():
    global zmeika_flag, zmeika_flag_2, training_zmeika, record_zmeika, direction_zmeika, zmeika_death_flag, \
        zmeika_pause_flag, schet, color_5, color_6, color_7, zmeika_apple_flag, color_8, FPS, color_9, sprites_zmeika, \
        sprites_zmeika_2, sprites_zmeika_3, sprites_zmeika_4, menu_flag
    fon = pygame.transform.scale(load_image('bg_menu.jpg'), (width, height))
    screen2.blit(fon, (0, 0))
    pygame.display.set_caption('Змейка')
    pygame.display.set_icon(pygame.image.load('data/ZMEIKA.ico'))
    # текст на экране
    intro_text = ['Обучение:',
                  '    Для запуска игры "Змейка" нажмите кнопку.',
                  '    Во время игры змейка будет ползти в направлении стрелки, чтобы',
                  'изменить ее направление используйте стрелки на клавиатуре или WASD.',
                  '    Собирайте красные яблоки, чтобы заработать очки и расти, после',
                  'смерти рекорд будет записан.',
                  '    При нажатие на кнопку или клавишу Escape, вы можете открыть меню',
                  'паузы. При нажатие на кнопку или клавишу Backspace, вы можете выйти',
                  'в меню, также можно и не из меню паузы. Также находясь в меню паузы',
                  'или экране смерти, используйте кнопки или клавиши Space и Enter,',
                  'чтобы продолжить или начать заново.',
                  '    Если вы врежетесь в самого в себя или в стену, то умрете.',
                  '    Чтобы увидеть это одноразовое окно и стереть результат,',
                  'нажмите кнопку "clear".',
                  '                           Для продолжение нажмите любую клавишу.']
    font = pygame.font.Font(None, 49)
    text_coord = 30

    # вывод текста на экран
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('#444244'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 20
        text_coord += intro_rect.height
        screen2.blit(string_rendered, intro_rect)

    # игровой цикл
    sprites_zmeika = pygame.sprite.Group()
    sprites_zmeika_2 = pygame.sprite.Group()
    sprites_zmeika_3 = pygame.sprite.Group()
    sprites_zmeika_4 = pygame.sprite.Group()
    zmeika_flag_2 = True
    zmeika_death_flag = False
    zmeika_pause_flag = False
    zmeika_apple_flag = False
    schet = 0
    FPS = 15
    direction_zmeika = 'left'
    board = Board(19, 19)
    training_zmeika, record_zmeika = data_zmeika()
    if training_zmeika == 'не пройдено':
        running = True
    else:
        running = False
    zmeika_arrow(sprites_zmeika)
    CClear(sprites_zmeika_2, game='zmeika')
    Pause(sprites_zmeika_2, x=1060, y=15, game='zmeika')
    Back(sprites_zmeika_2, x=1060, y=222, game='zmeika')
    Reset(sprites_zmeika_2, x=1060, y=120, game='zmeika')
    Reset(sprites_zmeika_3, x=900, y=290, game='zmeika')
    Back(sprites_zmeika_3, x=900, y=170, game='zmeika')
    Continues(sprites_zmeika_3, x=900, y=410, game='zmeika')
    Reset(sprites_zmeika_4, x=900, y=335, game='zmeika')
    Back(sprites_zmeika_4, x=900, y=215, game='zmeika')
    while zmeika_flag:
        while running:
            # обучение
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    click_sound.play()
                    clock.tick(10)
                    running = False
                    with open("data/zmeika.txt", mode='w', encoding='utf-8') as f:
                        f.writelines(f'Обучение: пройдено')
                        f.writelines('\n')
                        f.writelines(f'Рекорд: {record_zmeika}')
                    training_zmeika = 'пройдено'
            screen.blit(screen2, (0, 0))
            pygame.display.flip()
            clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                sprites_zmeika_4.update(event)
                sprites_zmeika_3.update(event)
                sprites_zmeika_2.update(event)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    if board.check(direction_zmeika, 'left'):
                        sprites_zmeika.update('left', event)
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    if board.check(direction_zmeika, 'right'):
                        sprites_zmeika.update('right', event)
                elif event.key == pygame.K_w or event.key == pygame.K_UP:
                    if board.check(direction_zmeika, 'up'):
                        sprites_zmeika.update('up', event)
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    if board.check(direction_zmeika, 'down'):
                        sprites_zmeika.update('down', event)
                if zmeika_flag_2 and not zmeika_pause_flag and not zmeika_death_flag:
                    if event.key == pygame.K_ESCAPE:
                        click_sound.play()
                        clock.tick(10)
                        zmeika_pause_flag = True
                        zmeika_flag_2 = False
                    if event.key == pygame.K_BACKSPACE:
                        click_sound.play()
                        clock.tick(10)
                        pygame.mixer.music.load(menu_music)
                        pygame.mixer.music.play(-1, 0.0, 1500)
                        menu_flag = True
                        zmeika_flag = False
                        menu_screen()
                elif not zmeika_flag_2 and zmeika_pause_flag and not zmeika_death_flag:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        click_sound.play()
                        clock.tick(10)
                        zmeika_pause_flag = False
                        zmeika_flag_2 = True
                    if event.key == pygame.K_BACKSPACE:
                        click_sound.play()
                        clock.tick(10)
                        pygame.mixer.music.load(menu_music)
                        pygame.mixer.music.play(-1, 0.0, 1500)
                        menu_flag = True
                        zmeika_flag = False
                        menu_screen()
                if zmeika_death_flag:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        zmeika()
                    if event.key == pygame.K_BACKSPACE:
                        click_sound.play()
                        clock.tick(10)
                        pygame.mixer.music.load(menu_music)
                        pygame.mixer.music.play(-1, 0.0, 1500)
                        menu_flag = True
                        zmeika_flag = False
                        menu_screen()
            elif event.type == pygame.MOUSEMOTION:
                if zmeika_flag_2:
                    if 15 < event.pos[0] < (15 + 200) and \
                            130 < event.pos[1] < (130 + 70):
                        color_5 = False
                    else:
                        color_5 = True
                    if 1060 < event.pos[0] < (1060 + 100) and \
                            15 < event.pos[1] < (15 + 100):
                        color_6 = False
                    else:
                        color_6 = True
                    if 1060 < event.pos[0] < (1060 + 100) and \
                            120 < event.pos[1] < (120 + 100):
                        color_8 = False
                    else:
                        color_8 = True
                    if 1060 < event.pos[0] < (1060 + 100) and \
                            225 < event.pos[1] < (225 + 100):
                        color_7 = False
                    else:
                        color_7 = True
                    sprites_zmeika_2.update(event)
                elif zmeika_pause_flag:
                    if 900 < event.pos[0] < (900 + 100) and \
                            305 < event.pos[1] < (305 + 100):
                        color_8 = False
                    else:
                        color_8 = True
                    if 900 < event.pos[0] < (900 + 100) and \
                            190 < event.pos[1] < (190 + 100):
                        color_7 = False
                    else:
                        color_7 = True
                    if 900 < event.pos[0] < (900 + 100) and \
                            420 < event.pos[1] < (420 + 100):
                        color_9 = False
                    else:
                        color_9 = True
                    sprites_zmeika_3.update(event)
                elif zmeika_death_flag:
                    if 900 < event.pos[0] < (900 + 100) and \
                            335 < event.pos[1] < (335 + 100):
                        color_8 = False
                    else:
                        color_8 = True
                    if 900 < event.pos[0] < (900 + 100) and \
                            215 < event.pos[1] < (215 + 100):
                        color_7 = False
                    else:
                        color_7 = True
                    sprites_zmeika_4.update(event)
        screen.blit(fon, (0, 0))
        if zmeika_flag_2:
            board.crawl(direction_zmeika)
            board.render()
            sprites_zmeika.draw(screen)
            sprites_zmeika_2.draw(screen)
            zmeika_text('game')
        elif zmeika_pause_flag:
            zmeika_text('pause')
            sprites_zmeika_3.draw(screen)
        elif zmeika_death_flag:
            zmeika_text('death')
            sprites_zmeika_4.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


# создания уровня лабиринта
def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == 'F':
                Tile('finish', x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


# создания уровня лабиринта
def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    if not os.path.isfile(filename):
        print(f"Файл с уровнем '{filename}' не найден")
        sys.exit()
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


# изображения спрайтов
tile_images = {
    'wall': load_image('cobble.jpg'),
    'empty': load_image('floor.jpg'),
    'finish': load_image('finish.jpg')
}
player_image = load_image('player_down.png')
player_image2 = load_image('player_up.png')
player_image3 = load_image('player_left.png')
player_image4 = load_image('player_right.png')


# спрайты преград и дорожек лабиринта
class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group)
        global tile_width, tile_height, finish
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 310, tile_height * pos_y + 30)
        if tile_type == 'wall':
            self.add(walls_group)
        if tile_type == 'finish':
            finish = [tile_width * pos_x + 310, tile_height * pos_y + 30]


# спрайт игрока лабиринта
class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 310, tile_height * pos_y + 30)

    # для движения игрока
    def moving(self, x, y, direction):
        if x != 0:
            player.rect.x += x
            if pygame.sprite.spritecollideany(player, walls_group):
                player.rect.x -= x
        if y != 0:
            player.rect.y += y
            if pygame.sprite.spritecollideany(player, walls_group):
                player.rect.y -= y
        if direction == 'down':
            self.image = player_image
        elif direction == 'up':
            self.image = player_image2
        elif direction == 'left':
            self.image = player_image3
        elif direction == 'right':
            self.image = player_image4
        self.check()

    # проверка на выход за границы
    def check(self):
        global time
        if player.rect.y <= 30:
            player.rect.y += step
        if player.rect.y >= 690:
            player.rect.y -= step
        if player.rect.x == finish[0] and player.rect.y == finish[1]:
            if maze_level_1:
                maze_record(time, 1)
            elif maze_level_2:
                maze_record(time, 2)
            elif maze_level_3:
                maze_record(time, 3)


# окно лабиринта
def maze():
    global maze_flag, training_maze, level_1_maze, level_2_maze, level_3_maze, color_10, color_11, \
        color_12, maze_level_1, maze_level_2, maze_level_3, step, player, tiles_group, player_group, \
        walls_group, maze_pause_flag, sprites_maze_2, color_5, sprites_maze, color_7, color_6, time, color_8, \
        sprites_maze_3, color_9, menu_flag
    fon = pygame.transform.scale(load_image('bg_menu.jpg'), (width, height))
    screen2.blit(fon, (0, 0))
    pygame.display.set_caption('Лабиринт')
    pygame.display.set_icon(pygame.image.load('data/maze.ico'))
    # текст на экране
    intro_text = ['Обучение:',
                  '    Для запуска игры "Лабиринт" нажмите кнопку.',
                  '    Во время игры вы будете управлять персонажем, чтобы изменить его',
                  'направление используйте стрелки на клавиатуре или WASD.',
                  '    При нажатие на кнопку или клавишу Escape, вы можете открыть меню',
                  'паузы. При нажатие на кнопку или клавишу Backspace, вы можете выйти',
                  'в меню, также можно и не из меню паузы. Также находясь в меню паузы',
                  'или экране смерти, используйте кнопки или клавиши Space и Enter, чтобы',
                  'продолжить или начать заново.',
                  '    Попытайтесь как можно скорее пройти уровень, после прохождения',
                  'результат будет записан.',
                  '    Чтобы увидеть это одноразовое окно и стереть результат, нажмите',
                  'кнопку "clear".',
                  '                           Для продолжение нажмите любую клавишу.']
    font = pygame.font.Font(None, 49)
    text_coord = 45

    # вывод текста на экран
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('#444244'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 20
        text_coord += intro_rect.height
        screen2.blit(string_rendered, intro_rect)

    # игровой цикл
    sprites_maze = pygame.sprite.Group()
    sprites_maze_2 = pygame.sprite.Group()
    sprites_maze_3 = pygame.sprite.Group()
    btn_level_maze(sprites_maze, level=1)
    btn_level_maze(sprites_maze, level=2)
    btn_level_maze(sprites_maze, level=3)
    map_level_maze(sprites_maze, level=1)
    map_level_maze(sprites_maze, level=2)
    map_level_maze(sprites_maze, level=3)
    CClear(sprites_maze, x=910, y=550, game='maze')
    CClear(sprites_maze_2, game='level')
    Back(sprites_maze, x=1140, y=535, game='maze')
    Pause(sprites_maze_2, x=1075, y=15, game='maze')
    Reset(sprites_maze_2, x=1075, y=120, game='maze')
    Back(sprites_maze_2, x=1075, y=225, game='level')
    Reset(sprites_maze_3, x=900, y=290, game='maze')
    Back(sprites_maze_3, x=900, y=170, game='level')
    Continues(sprites_maze_3, x=900, y=410, game='maze')
    while maze_flag:
        i = 0
        time = 0
        player = None
        tiles_group = pygame.sprite.Group()
        player_group = pygame.sprite.Group()
        walls_group = pygame.sprite.Group()
        if training_maze == 'не пройдено':
            running = True
        else:
            running = False
        while maze_level_1 or maze_level_2 or maze_level_3:
            while running:
                # обучение
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        terminate()
                    elif event.type == pygame.KEYDOWN or \
                            event.type == pygame.MOUSEBUTTONDOWN:
                        click_sound.play()
                        clock.tick(10)
                        running = False
                        with open("data/maze.txt", mode='w', encoding='utf-8') as f:
                            f.writelines(f'Обучение: пройдено')
                            f.writelines('\n')
                            f.writelines(f'1 уровень: {level_1_maze[0]} - {level_1_maze[1]}')
                            f.writelines('\n')
                            f.writelines(f'2 уровень: {level_2_maze[0]} - {level_2_maze[1]}')
                            f.writelines('\n')
                            f.writelines(f'3 уровень: {level_3_maze[0]} - {level_3_maze[1]}')
                        training_maze = 'пройдено'
                screen.blit(screen2, (0, 0))
                pygame.display.flip()
                clock.tick(FPS)
            if i == 0:
                i += 1
                if maze_level_1:
                    player, level_x, level_y = generate_level(load_level('level1.txt'))
                elif maze_level_2:
                    player, level_x, level_y = generate_level(load_level('level2.txt'))
                elif maze_level_3:
                    player, level_x, level_y = generate_level(load_level('level3.txt'))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == MYEVENTTYPE and not maze_pause_flag:
                    time += 1
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    sprites_maze_2.update(event)
                    sprites_maze_3.update(event)
                elif event.type == pygame.MOUSEMOTION:
                    if not maze_pause_flag:
                        if 15 < event.pos[0] < (15 + 200) and \
                                130 < event.pos[1] < (130 + 70):
                            color_5 = False
                        else:
                            color_5 = True
                        if 1075 < event.pos[0] < (1075 + 100) and \
                                15 < event.pos[1] < (15 + 100):
                            color_6 = False
                        else:
                            color_6 = True
                        if 1075 < event.pos[0] < (1075 + 100) and \
                                120 < event.pos[1] < (120 + 100):
                            color_8 = False
                        else:
                            color_8 = True
                        if 1075 < event.pos[0] < (1075 + 100) and \
                                225 < event.pos[1] < (225 + 100):
                            color_7 = False
                        else:
                            color_7 = True
                        sprites_maze_2.update(event)
                    else:
                        if 900 < event.pos[0] < (900 + 100) and \
                                290 < event.pos[1] < (290 + 100):
                            color_8 = False
                        else:
                            color_8 = True
                        if 900 < event.pos[0] < (900 + 100) and \
                                170 < event.pos[1] < (170 + 100):
                            color_7 = False
                        else:
                            color_7 = True
                        if 900 < event.pos[0] < (900 + 100) and \
                                410 < event.pos[1] < (410 + 100):
                            color_9 = False
                        else:
                            color_9 = True
                        sprites_maze_3.update(event)
                elif event.type == pygame.KEYDOWN:
                    if maze_pause_flag:
                        if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            click_sound.play()
                            clock.tick(10)
                            maze_pause_flag = False
                    else:
                        if event.key == pygame.K_ESCAPE:
                            click_sound.play()
                            clock.tick(10)
                            maze_pause_flag = True
                    if event.key == pygame.K_BACKSPACE:
                        click_sound.play()
                        clock.tick(10)
                        maze_pause_flag = False
                        maze_level_1 = False
                        maze_level_2 = False
                        maze_level_3 = False
                    if (event.key == pygame.K_a or event.key == pygame.K_LEFT) and not maze_pause_flag:
                        player.moving(-step, 0, 'left')
                    elif (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and not maze_pause_flag:
                        player.moving(step, 0, 'right')
                    elif (event.key == pygame.K_w or event.key == pygame.K_UP) and not maze_pause_flag:
                        player.moving(0, -step, 'up')
                    elif (event.key == pygame.K_s or event.key == pygame.K_DOWN) and not maze_pause_flag:
                        player.moving(0, step, 'down')
            screen.blit(fon, (0, 0))
            if not maze_pause_flag:
                tiles_group.draw(screen)
                player_group.draw(screen)
                sprites_maze_2.draw(screen)
                maze_text('level', time)
            else:
                maze_text('pause')
                sprites_maze_3.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                sprites_maze.update(event)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    click_sound.play()
                    clock.tick(10)
                    pygame.mixer.music.load(menu_music)
                    pygame.mixer.music.play(-1, 0.0, 1500)
                    menu_flag = True
                    maze_flag = False
                    menu_screen()
            elif event.type == pygame.MOUSEMOTION:
                if 170 < event.pos[0] < (170 + 200) and \
                        height // 2 < event.pos[1] < (height // 2 + 100):
                    color_10 = False
                else:
                    color_10 = True
                if 540 < event.pos[0] < (540 + 200) and \
                        height // 2 < event.pos[1] < (height // 2 + 100):
                    color_11 = False
                else:
                    color_11 = True
                if 910 < event.pos[0] < (910 + 200) and \
                        height // 2 < event.pos[1] < (height // 2 + 100):
                    color_12 = False
                else:
                    color_12 = True
                if 1140 < event.pos[0] < (1140 + 100) and \
                        535 < event.pos[1] < (535 + 100):
                    color_7 = False
                else:
                    color_7 = True
                if 910 < event.pos[0] < (910 + 200) and \
                        550 < event.pos[1] < (550 + 100):
                    color_5 = False
                else:
                    color_5 = True
                sprites_maze.update(event)
        screen.blit(fon, (0, 0))
        sprites_maze.draw(screen)
        maze_text('game')
        pygame.display.flip()
        clock.tick(50)
    pygame.quit()


# окно Шашок
def shashki():
    global shashki_flag, menu_flag
    pygame.mixer.music.load(shashki_music)
    pygame.mixer.music.play(-1, 0.0, 1500)
    fon = pygame.transform.scale(load_image('bg_menu.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    pygame.display.set_caption('Шашки')
    pygame.display.set_icon(pygame.image.load('data/shashki.ico'))
    # текст на экране
    propysk = '                                        '
    intro_text = ['coming soon.....']
    font = pygame.font.Font(None, 80)
    text_coord = height // 2

    # вывод текста на экран
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('#444244'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = width // 2 - intro_rect.width // 2
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    # игровой цикл
    while shashki_flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()
                clock.tick(10)
                shashki_flag = False
                menu_flag = True
                pygame.mixer.music.load(menu_music)
                pygame.mixer.music.play(-1, 0.0, 1500)
                menu_screen()
        pygame.display.flip()
        clock.tick(50)
    pygame.quit()


start_screen()
