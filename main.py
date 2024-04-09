from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.core.window import Window
import pygame.mixer
import numpy as np

class VirtualPiano(App):
    def build(self):
        # Основной контейнер, который будет содержать два контейнера для слайдера и клавиш
        main_layout = BoxLayout(orientation='vertical')

        # Верхний контейнер для слайдера
        slider_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50)
        main_layout.add_widget(slider_layout)

        # Создаем слайдер для регулировки громкости
        volume_slider = Slider(min=0, max=1, value=1, orientation='horizontal')
        volume_slider.bind(value=self.on_volume_change)
        slider_layout.add_widget(volume_slider)

        # Нижний контейнер для клавиш
        keys_layout = GridLayout(cols=12, spacing=5, size_hint=(1, None), height=Window.height - 50)
        keys_layout.padding = [0, 10, 0, 0]  # Добавляем отступ сверху
        main_layout.add_widget(keys_layout)

        # Устанавливаем белый цвет фона для всего окна
        Window.clearcolor = (1, 1, 1, 1)

        # Инициализация звукового движка Pygame
        pygame.mixer.init()

        # Инициализация громкости
        self.volume = 1

        # Создаем кнопки для клавиш
        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        for note in notes:
            button = Button(text=note, background_color=self.button_color(note))
            button.background_color_normal = button.background_color  # Цвет фона в обычном состоянии
            button.background_color_down = (0.5, 0.5, 0.5, 1)  # Более яркий цвет при нажатии
            button.bind(on_press=lambda instance, note=note: self.play_sound(note))  # Привязываем функцию play_sound к нажатию кнопки
            keys_layout.add_widget(button)

        return main_layout

    def on_start(self):
        Window.size = (1920, 1080)  # Устанавливаем размер окна приложения
        Window.minimum_width = Window.size[0]  # Фиксируем минимальную ширину окна
        Window.minimum_height = Window.size[1]  # Фиксируем минимальную высоту окна

    def play_sound(self, note):
        # Определение частоты для каждой ноты
        frequencies = {'C': 261.63, 'C#': 277.18, 'D': 293.66, 'D#': 311.13, 'E': 329.63, 'F': 349.23,
                       'F#': 369.99, 'G': 392.00, 'G#': 415.30, 'A': 440.00, 'A#': 466.16, 'B': 493.88}

        # Генерация синусоидальной волны для данной частоты и длительности
        duration = 1.0  # Продолжительность звука в секундах
        sample_rate = 44100  # Частота дискретизации
        t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
        wave = np.sin(2 * np.pi * frequencies[note] * t)

        # Преобразование массива numpy в объект pygame Sound
        sound = pygame.mixer.Sound(wave.astype(np.float32))
        sound.set_volume(self.volume)  # Устанавливаем громкость звука
        sound.play()

    def on_volume_change(self, instance, volume):
        # Обновляем громкость при изменении слайдера
        self.volume = volume

    def button_color(self, note):
        if '#' in note:
            return (0.5, 0.5, 0.5, 1)  # Темный цвет для кнопок с решеткой
        else:
            return (2, 2, 2, 1)  # Светлый цвет для кнопок без решетки

if __name__ == '__main__':
    VirtualPiano().run()
