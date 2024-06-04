from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.image import Image as CoreImage
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import AsyncImage, Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget
from random import uniform
from tkinter import Tk
import os
import random
import json

with open('settings.json', 'r') as f:
    data = json.load(f)
    settings = data

diff = float
win = Tk()
screen_width = win.winfo_screenwidth()
screen_height = win.winfo_screenheight()

Window.fullscreen = 'auto'
ROWS = 23
COLS = 19
FPS = 24

BLACK = (0.082, 0.094, 0.114)
BLUE = (0.122, 0.098, 0.298)
RED = (0.988, 0.357, 0.478)
WHITE = (1, 1, 1)

img_paths = [
    'sourses/figures/1.png',
    'sourses/figures/2.png',
    'sourses/figures/3.png',
    'sourses/figures/4.png',
    'sourses/figures/5.png',
    'sourses/figures/6.png'
]
Assets = {}

font_path = 'sourses/Alternity-8w7J.ttf'

for i, path in enumerate(img_paths):
    if os.path.exists(path):
        Assets[i + 1] = CoreImage(path).texture
    else:
        print()

class Tetramino:
    FIGURES = {
        'I': [[1, 5, 9, 13], [4, 5, 6, 7]],
        'Z': [[4, 5, 9, 10], [2, 6, 5, 9]],
        'S': [[6, 7, 9, 10], [1, 5, 6, 10]],
        'L': [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        'J': [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        'T': [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        'O': [[1, 2, 5, 6]]
    }
    TYPES = list(FIGURES.keys())

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.choice(self.TYPES)
        self.shape = self.FIGURES[self.type]
        self.color = random.randint(1, 6)
        self.rotation = 0

    def image(self):
        return self.shape[self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape)

class TetrisGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rows = ROWS
        self.cols = COLS
        self.score = 0
        self.level = int(1)
        self.board = [[0 for j in range(COLS)] for i in range(ROWS)]
        self.next = None
        self.gameover = False
        self.new_figure()
        self.counter = 0
        self.move_down = False
        self.can_move = True
        Clock.schedule_interval(self.update, 1.0 / FPS)
        self.bind(size=self.update_canvas, pos=self.update_canvas)
        self.update_canvas()

    def update_canvas(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(*BLACK)
            Rectangle(pos=self.pos, size=self.size)

            Color(*WHITE)
            for i in range(self.rows):
                Line(points=[580/1920*screen_width, (i*40+40)/1080*screen_height, 1340/1920*screen_width, (i*40+40)/1080*screen_height], width=1)
            for j in range(self.cols + 1):
                Line(points=[(j*40+580)/1920*screen_width, 40/1080*screen_height, (j*40+580)/1920*screen_width, 920/1080*screen_height], width=1)

            for x in range(self.rows):
                for y in range(self.cols):
                    if self.board[x][y] > 0:
                        val = self.board[x][y]
                        img = Assets.get(val)
                        if img:
                            Rectangle(texture=img, pos=((y*40+580)/1920*screen_width, (920-x*40)/1080*screen_height), size=(40/1920*screen_width, 40/1080*screen_height))
                        Line(rectangle=((y*40+580)/1920*screen_width, (920-x*40)/1080*screen_height, 40/1920*screen_width, 40/1080*screen_height), width=1, color=Color(*WHITE))

            if self.figure:
                for i in range(4):
                    for j in range(4):
                        if i * 4 + j in self.figure.image():
                            img = Assets.get(self.figure.color)
                            if img:
                                x = 40 * (self.figure.x + j)
                                y = 40 * (self.figure.y + i)
                                Rectangle(texture=img, pos=((580+x)/1920*screen_width, (920-y)/1080*screen_height), size=(40/1920*screen_width, 40/1080*screen_height))
                                Line(rectangle=((580+x)/1920*screen_width, (920-y)/1080*screen_height, 40/1920*screen_width, 40/1080*screen_height), width=1, color=Color(*WHITE))

            Color(*BLUE)
            Rectangle(pos=(1, 920/1080*screen_height), size=(1920/1920*screen_width, 160/1080*screen_height))

            self.add_widget(Label(text=str(self.score), font_size=100*(screen_width/1920), color=WHITE, pos=(100/1920*screen_width, 950/1080*screen_height)))
            self.add_widget(Label(text=f'Складність : {self.level}', font_size=50*(screen_width/1920), color=WHITE, pos=(1660/1920*screen_width, 950/1080*screen_height)))

            if self.next:
                for i in range(4):
                    for j in range(4):
                        if i * 4 + j in self.next.image():
                            img = Assets.get(self.next.color)
                            if img:
                                x = 40 * (j + 1)
                                y = 40 * (3 - i)
                                Rectangle(texture=img, pos=((950-90+x)/1920*screen_width, (920+y)/1080*screen_height), size=(40/1920*screen_width, 40/1080*screen_height))
                                Line(rectangle=((950-90+x)/1920*screen_width, (920+y)/1080*screen_height, 40/1920*screen_width, 40/1080*screen_height), width=1, color=Color(*WHITE))

            if self.gameover:
                self.sound_player = MusicPlayer()
                self.sound_player.sound9.play()
                Color(*BLACK)
                rect = (775/1920*screen_width, 425/1080*screen_height, 370/1920*screen_width, 230/1080*screen_height)
                Rectangle(pos=(rect[0], rect[1]), size=(rect[2], rect[3]))
                Line(rectangle=rect, width=2, color=Color(*RED))
                self.add_widget(Label(text='Гра закінчена', font_size=40*(screen_width/1920), color=WHITE, pos=((rect[0] + rect[2] // 3), rect[1] + rect[3] // 2)))
                self.add_widget(Label(text='Натисніть r, щоб розпочати знову ', font_size=20*(screen_width/1920), color=RED, pos=((rect[0] + rect[2] // 3), rect[1] + rect[3] // 3.5)))
                self.add_widget(Label(text='Натисніть q, щоб вийти', font_size=20*(screen_width/1920), color=RED, pos=((rect[0] + rect[2] // 3), rect[1] + rect[3] // 9)))

    def new_figure(self):
        if not self.next:
            self.next = Tetramino(5, 0)
        self.figure = self.next
        self.next = Tetramino(5, 0)
        if self.intersects():
            self.figure.y -= 3
            if self.intersects():
                self.gameover = True

    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if (i + self.figure.y >= self.rows or j + self.figure.x >= self.cols or j + self.figure.x < 0 or self.board[i + self.figure.y][j + self.figure.x] > 0):
                        intersection = True
        return intersection

    def remove_line(self):
        global diff
        rerun = False
        for y in range(self.rows - 1, -1, -1):
            is_full = True
            for x in range(self.cols):
                if self.board[y][x] == 0:
                    is_full = False
            if is_full:
                self.sound_player = MusicPlayer()
                self.sound_player.sound8.play()
                del self.board[y]
                self.board.insert(0, [0 for _ in range(self.cols)])
                self.score += 15*diff
                rerun = True

        if rerun:
            self.remove_line()

    def freeze(self):
        global diff
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.board[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.score += 4
        self.level = int(1 + (self.score // (250 / diff)))
        self.remove_line()
        self.new_figure()
        if self.intersects():
            self.gameover = True

    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        self.sound_player = MusicPlayer()
        self.sound_player.sound5.play()
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def go_side(self, dx):
        self.figure.x += dx
        if self.intersects():
            self.figure.x -= dx

    def rotate(self):
        rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = rotation

    def update(self, dt):
        self.counter += 1
        if self.counter >= 10000:
            self.counter = 0

        if self.can_move:
            if self.counter % (FPS // (self.level * 2)) == 0 or self.move_down:
                if not self.gameover:
                    self.go_down()
        self.update_canvas()

    def on_key_down(self, keyboard, keycode, text, modifiers):
        if self.can_move and not self.gameover:
            if keycode[1] == str(settings['BTN1']):
                self.sound_player = MusicPlayer()
                self.sound_player.sound5.play()
                self.go_side(-1)
            elif keycode[1] == str(settings['BTN2']):
                self.sound_player = MusicPlayer()
                self.sound_player.sound5.play()
                self.go_side(1)
            elif keycode[1] == str(settings['BTN3']):
                self.sound_player = MusicPlayer()
                self.sound_player.sound6.play()
                self.rotate()
            elif keycode[1] == str(settings['BTN4']):
                self.move_down = True
            elif keycode[1] == str(settings['BTN5']):
                self.sound_player = MusicPlayer()
                self.sound_player.sound7.play()
                self.go_space()
        if keycode[1] == 'r':
            self.__init__()
        if keycode[1] == 'p':
            self.can_move = not self.can_move
        if keycode[1] == 'q':
            self.__init__()
            self.can_move = not self.can_move
            parent_widget = self.parent
            while not isinstance(parent_widget, ScreenManager):
                parent_widget = parent_widget.parent
            parent_widget.current = 'main'

    def on_key_up(self, keyboard, keycode):
        if keycode[1] == str(settings['BTN4']):
            self.move_down = False

class TetrisScreen(Screen):
    def on_enter(self):
        self.game = TetrisGame()
        self.add_widget(self.game)
        self.keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self.keyboard.bind(on_key_down=self.game.on_key_down, on_key_up=self.game.on_key_up)

    def _keyboard_closed(self):
        self.keyboard.unbind(on_key_down=self.game.on_key_down, on_key_up=self.game.on_key_up)
        self.keyboard = None

    def on_leave(self):
        if self.keyboard:
            self.keyboard.release()
            self.keyboard = None
        self.remove_widget(self.game)

class MusicPlayer:
    def __init__(self):
        self.music = SoundLoader.load('sourses/sounds/main_back.wav')
        self.sound1 = SoundLoader.load('sourses/sounds/press_button.wav')
        self.sound2 = SoundLoader.load('sourses/sounds/level1_2.wav')
        self.sound3 = SoundLoader.load('sourses/sounds/level3_4.wav')
        self.sound4 = SoundLoader.load('sourses/sounds/level5.wav')
        self.sound5 = SoundLoader.load('sourses/sounds/moving_figures.wav')
        self.sound6 = SoundLoader.load('sourses/sounds/rotation_figures.wav')
        self.sound7 = SoundLoader.load('sourses/sounds/get_down.wav')
        self.sound8 = SoundLoader.load('sourses/sounds/delete_line.wav')
        self.sound9 = SoundLoader.load('sourses/sounds/end.wav')
        self.music.bind(on_stop=self.play_music)
        self.load_settings()

    def play_music(self, *args):
        if self.music.state != 'play':
            self.music.play()

    def load_settings(self):
        try:
            self.music.volume = settings['MUSIC_VOLUME']
            self.sound1.volume = settings['SOUND_VOLUME']
            self.sound2.volume = settings['SOUND_VOLUME']
            self.sound3.volume = settings['SOUND_VOLUME']
            self.sound4.volume = settings['SOUND_VOLUME']
            self.sound5.volume = settings['SOUND_VOLUME'] / 3
            self.sound6.volume = settings['SOUND_VOLUME']
            self.sound7.volume = settings['SOUND_VOLUME']
            self.sound8.volume = settings['SOUND_VOLUME']
            self.sound9.volume = settings['SOUND_VOLUME']
        except ImportError:
            self.music.volume = 0.5
            self.sound1.volume = 0.5
            self.sound2.volume = 0.5
            self.sound3.volume = 0.5
            self.sound4.volume = 0.5
            self.sound5.volume = 0.25
            self.sound6.volume = 0.5
            self.sound7.volume = 0.5
            self.sound8.volume = 0.5
            self.sound9.volume = 0.5

class MainPage(Screen):
    def __init__(self, **kwargs):
        super(MainPage, self).__init__(**kwargs)
        Window.fullscreen = 'auto'
        layout_img = BoxLayout(orientation='vertical', spacing=30/1080*screen_height, padding=(25/1920*screen_width, 10/1080*screen_height, 330/1920*screen_width, 500/1080*screen_height))
        self.img = AsyncImage(source="sourses/tetris.png", size_hint=(1.2, 1.2), allow_stretch=True)
        layout = BoxLayout(orientation='vertical', spacing=30/1080*screen_height, padding=(10/1920*screen_width, 250/1080*screen_height, 10/1920*screen_width, 250/1080*screen_height))
        self.btn1 = Button(text='Один гравець', on_press=self.player1, size_hint=(None, None), size=(170/1920*screen_width, 50/1080*screen_height), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.btn2 = Button(text='Налаштування', on_press=self.options, size_hint=(None, None), size=(170/1920*screen_width, 50/1080*screen_height), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.btn3 = Button(text='Інше', on_press=self.other, size_hint=(None, None), size=(170/1920*screen_width, 50/1080*screen_height), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.btn4 = Button(text='Вихід', on_press=self.exit, size_hint=(None, None), size=(170/1920*screen_width, 50/1080*screen_height), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.figures = [f for f in os.listdir('sourses/figures') if f.endswith('.png')]
        Clock.schedule_interval(self.Falling, 1/10)
        layout.add_widget(self.btn1)
        layout.add_widget(self.btn2)
        layout.add_widget(self.btn3)
        layout.add_widget(self.btn4)
        layout_img.add_widget(self.img)
        self.add_widget(layout_img)
        self.add_widget(layout)

    def player1(self, instance):
        self.sound_player = MusicPlayer()
        self.sound_player.sound1.play()
        self.manager.current = 'page1'

    def options(self, instance):
        self.sound_player = MusicPlayer()
        self.sound_player.sound1.play()
        self.manager.current = 'page2'

    def other(self, instance):
        self.sound_player = MusicPlayer()
        self.sound_player.sound1.play()
        self.manager.current = 'page3'

    def exit(self, instance):
        self.sound_player = MusicPlayer()
        self.sound_player.sound1.play()
        App.get_running_app().stop()

    def Falling(self, *args):
        figure_path = os.path.join('sourses/figures', random.choice(self.figures))
        image = Image(source=figure_path)
        i= random.randrange(-100, 100)
        if (i % 2):
            image.center_x = random.randrange(-1000, -250)
        else:
            image.center_x =  random.randrange(250, 1000)
        image.y = Window.height
        image.rotation = uniform(-45, 45)
        anim = Animation(center_y=-100, duration=5)
        anim.start(image)
        self.add_widget(image)
        return image

class Page1(Screen):
    def __init__(self, **kwargs):
        super(Page1, self).__init__(**kwargs)
        layout_img = BoxLayout(orientation='vertical', spacing=30/1080*screen_height, padding=(25/1920*screen_width, 10/1080*screen_height, 330/1920*screen_width, 500/1080*screen_height))
        self.img = AsyncImage(source="sourses/tetris.png", size_hint=(1.2, 1.2), allow_stretch=True)
        layout = BoxLayout(orientation='vertical', spacing=30/1080*screen_height, padding=(10/1920*screen_width, 250/1080*screen_height, 10/1920*screen_width, 250/1080*screen_height))
        self.lbl1 = Label(text='Оберіть складність гри:', size_hint=(None, None), size=(170/1920*screen_width, 50/1080*screen_height), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.btn1 = Button(text='Не відчуваю', on_press=self.level1, size_hint=(None, None), size=(170/1920*screen_width, 50/1080*screen_height), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.btn2 = Button(text='Легкий', on_press=self.level2,  size_hint=(None, None), size=(170/1920*screen_width, 50/1080*screen_height), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.btn3 = Button(text='Нормальок', on_press=self.level3, size_hint=(None, None), size=(170/1920*screen_width, 50/1080*screen_height), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.btn4 = Button(text='Напряжненько', on_press=self.level4, size_hint=(None, None), size=(170/1920*screen_width, 50/1080*screen_height),  pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.btn5 = Button(text='єШлях...', on_press=self.level5, size_hint=(None, None), size=(170/1920*screen_width, 50/1080*screen_height), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        layout_mbtn = BoxLayout(orientation='vertical', spacing=10/1080*screen_height, padding=(10/1920*screen_width, 500/1080*screen_height, 10/1920*screen_width, 10/1080*screen_height))
        mbtn = Button(text='До головної', on_press=self.go_to_main_page, size_hint=(None, None), size=(135/1920*screen_width, 30/1080*screen_height), pos_hint={'center_x': 0.9, 'center_y': 0.5})
        layout.add_widget(self.lbl1)
        layout.add_widget(self.btn1)
        layout.add_widget(self.btn2)
        layout.add_widget(self.btn3)
        layout.add_widget(self.btn4)
        layout.add_widget(self.btn5)
        layout_img.add_widget(self.img)
        layout_mbtn.add_widget(mbtn)
        self.add_widget(layout_img)
        self.add_widget(layout)
        self.add_widget(layout_mbtn)

    def go_to_main_page(self, instance):
        self.sound_player = MusicPlayer()
        self.sound_player.sound1.play()
        self.manager.current = 'main'

    def level1(self, instance):
        global diff
        self.sound_player = MusicPlayer()
        self.sound_player.sound2.play()
        diff=1
        self.manager.current = 'tetris'

    def level2(self, instance):
        global diff
        self.sound_player = MusicPlayer()
        self.sound_player.sound2.play()
        diff=1.15
        self.manager.current = 'tetris'

    def level3(self, instance):
        global diff
        self.sound_player = MusicPlayer()
        self.sound_player.sound3.play()
        diff = 1.25
        self.manager.current = 'tetris'

    def level4(self, instance):
        global diff
        self.sound_player = MusicPlayer()
        self.sound_player.sound3.play()
        diff = 1.5
        self.manager.current = 'tetris'

    def level5(self, instance):
        global diff
        self.sound_player = MusicPlayer()
        self.sound_player.sound4.play()
        diff = 2
        self.manager.current = 'tetris'

class Page2(Screen):
    def __init__(self, **kwargs):
        super(Page2, self).__init__(**kwargs)
        main_layout = BoxLayout(orientation='vertical', spacing=25/1080*screen_height, padding=(30/1920*screen_width, 15/1080*screen_height, 30/1920*screen_width, 30/1080*screen_height))
        music_layout = BoxLayout(orientation='horizontal')
        self.music_slider = Slider(min=0, max=1, value=0.5)
        self.sound_slider = Slider(min=0, max=1, value=0.5)
        music_label = Label(text='Музика')
        sound_label = Label(text='Звуки')
        music_layout.add_widget(music_label)
        music_layout.add_widget(self.music_slider)
        music_layout.add_widget(sound_label)
        music_layout.add_widget(self.sound_slider)
        main_layout.add_widget(music_layout)
        self.music_slider.value = settings['MUSIC_VOLUME']
        self.sound_slider.value = settings['SOUND_VOLUME']
        layout_1 = GridLayout(cols=2, spacing=10/1080*screen_height, padding=(740/1920*screen_width, 30/1080*screen_height, 740/1920*screen_width, 30/1080*screen_height))
        label_1 = Label(text='Пересунути вліво:', size_hint=(None, None), size=(170/1920*screen_width, 30/1080*screen_height))
        self.inp1 = Button(text=settings['BTN1'], on_press=self.select_button1, size=(200/1920*screen_width, 30/1080*screen_height))
        label_2 = Label(text='Пересунути вправо:', size_hint=(None, None), size=(170/1920*screen_width, 30/1080*screen_height))
        self.inp2 = Button(text=settings['BTN2'], on_press=self.select_button2, size=(200/1920*screen_width, 30/1080*screen_height))
        label_3 = Label(text='Перевернути:', size_hint=(None, None), size=(170/1920*screen_width, 30/1080*screen_height))
        self.inp3 = Button(text=settings['BTN3'], on_press=self.select_button3, size=(200/1920*screen_width, 30/1080*screen_height))
        label_4 = Label(text='Пришвидшити:', size_hint=(None, None), size=(170/1920*screen_width, 30/1080*screen_height))
        self.inp4 = Button(text=settings['BTN4'], on_press=self.select_button4, size=(200/1920*screen_width, 30/1080*screen_height))
        label_5 = Label(text='Швидко до низу:', size_hint=(None, None), size=(170/1920*screen_width, 30/1080*screen_height))
        self.inp5 = Button(text=settings['BTN5'], on_press=self.select_button5, size=(200/1920*screen_width, 30/1080*screen_height))

        layout_1.add_widget(label_1)
        layout_1.add_widget(self.inp1)
        layout_1.add_widget(label_2)
        layout_1.add_widget(self.inp2)
        layout_1.add_widget(label_3)
        layout_1.add_widget(self.inp3)
        layout_1.add_widget(label_4)
        layout_1.add_widget(self.inp4)
        layout_1.add_widget(label_5)
        layout_1.add_widget(self.inp5)
        main_layout.add_widget(layout_1)

        layout_mbtn = GridLayout(cols=1, spacing=10 / 1080 * screen_height, padding=(850 / 1920 * screen_width, 100 / 1080 * screen_height, 10 / 1920 * screen_width, 400 / 1080 * screen_height))
        mbtn = Button(text='До головної', on_press=self.go_to_main_page, size_hint=(None, None), size=(150 / 1920 * screen_width, 60 / 1080 * screen_height), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        layout_mbtn.add_widget(mbtn)
        main_layout.add_widget(layout_mbtn)
        self.add_widget(main_layout)

        layout_achtung = BoxLayout(orientation='vertical', spacing=10 / 1080 * screen_height, padding=(10 / 1920 * screen_width, 500 / 1080 * screen_height, 10 / 1920 * screen_width, 530 / 1080 * screen_height))
        achtung = Label(text="УВАГА!\nНе обирайте кнопки 'q', 'r' та 'p'!\nВони вже використовуються в програмі.", size=(135 / 1920 * screen_width, 30 / 1080 * screen_height), pos_hint={'center_x': 0.9, 'center_y': 0.5})
        layout_achtung.add_widget(achtung)
        self.add_widget(layout_achtung)

        Clock.schedule_interval(self.update_music_volume, 0.1)

    def select_button1(self, instance):
        self.inp1.text = 'Натисніть клавішу...'
        self.bind_keyboard_for_button(self.inp1)

    def select_button2(self, instance):
        self.inp2.text = 'Натисніть клавішу...'
        self.bind_keyboard_for_button(self.inp2)

    def select_button3(self, instance):
        self.inp3.text = 'Натисніть клавішу...'
        self.bind_keyboard_for_button(self.inp3)

    def select_button4(self, instance):
        self.inp4.text = 'Натисніть клавішу...'
        self.bind_keyboard_for_button(self.inp4)

    def select_button5(self, instance):
        self.inp5.text = 'Натисніть клавішу...'
        self.bind_keyboard_for_button(self.inp5)

    def bind_keyboard_for_button(self, button):
        keyboard = Window.request_keyboard(self._keyboard_closed, self)
        keyboard.bind(on_key_down=self.on_key_down)

        self.active_button = button

    def on_key_down(self, keyboard, keycode, text, modifiers):
        if self.active_button:
            self.active_button.text = keycode[1]
            self.unbind_keyboard()

    def unbind_keyboard(self):
        self.active_button = None
        Window.unbind(on_key_down=self.on_key_down)

    def _keyboard_closed(self):
        self.unbind_keyboard()

    def go_to_main_page(self, instance):
        self.sound_player = MusicPlayer()
        self.sound_player.sound1.play()

        settings['MUSIC_VOLUME'] = self.music_slider.value
        settings['SOUND_VOLUME'] = self.sound_slider.value
        settings['BTN1'] = self.inp1.text
        settings['BTN2'] = self.inp2.text
        settings['BTN3'] = self.inp3.text
        settings['BTN4'] = self.inp4.text
        settings['BTN5'] = self.inp5.text

        with open('settings.json', 'w') as f:
            json.dump(settings, f)

        app = App.get_running_app()
        app.music_player.music.volume = self.music_slider.value
        app.sound_player.music.volume = self.sound_slider.value
        self.manager.current = 'main'

    def update_music_volume(self, *args):
        self.sound_player = MusicPlayer()
        app = App.get_running_app()
        app.music_player.music.volume = self.music_slider.value
        app.sound_player.music.volume = self.sound_slider.value

class Page3(Screen):
    def __init__(self, **kwargs):
        super(Page3, self).__init__(**kwargs)
        layout_info = BoxLayout(orientation='vertical', spacing=10 / 1080 * screen_height, padding=(10 / 1920 * screen_width, 200 / 1080 * screen_height, 10 / 1920 * screen_width, 200 / 1080 * screen_height))
        img = Image(source='sourses/logo_page3.png')
        layout_info.add_widget(img)
        mlbl = Label(text='Ця програма є курсовим проєктом студентів групи ІО-25 - Коваля Костянтина та Дейкала Владислава\n'
                 'Метою проєкту було створення гри, використовуючи зручну для нас мову програмування Python.\n'
                 'В ході створення програми виникали проблеми, які було цікаво вирішувати, зокрема проблема з вікном налаштувань.\n'
                 'Хотілося б відмітити, що програма повністю написана на мові Python, використовуючи тільки її бібліотеки.\n'
                 'Проєкт було створено виключно із розважальних цілей та власних інтересів.', font_size=34, halign='center')
        layout_info.add_widget(mlbl)
        self.add_widget(layout_info)

        layout_mbtn = BoxLayout(orientation='vertical', spacing=10 / 1080 * screen_height, padding=(10 / 1920 * screen_width, 500 / 1080 * screen_height, 10 / 1920 * screen_width, 10 / 1080 * screen_height))
        mbtn = Button(text='До головної', on_press=self.go_to_main_page, size_hint=(None, None), size=(135 / 1920 * screen_width, 30 / 1080 * screen_height), pos_hint={'center_x': 0.9, 'center_y': 0.5})
        layout_mbtn.add_widget(mbtn)
        self.add_widget(layout_mbtn)

    def go_to_main_page(self, instance):
        self.sound_player = MusicPlayer()
        self.sound_player.sound1.play()
        self.manager.current = 'main'

class MyApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.music_player = MusicPlayer()
        self.sound_player = MusicPlayer()
        self.music_player.play_music()

    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainPage(name='main'))
        sm.add_widget(Page1(name='page1'))
        sm.add_widget(Page2(name='page2'))
        sm.add_widget(Page3(name='page3'))
        sm.add_widget(TetrisScreen(name='tetris'))
        return sm

if __name__ == '__main__':
    MyApp().run()