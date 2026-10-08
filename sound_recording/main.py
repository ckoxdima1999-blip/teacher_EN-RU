import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator
import random


duration = 5  # секунды записи
sample_rate = 44100
words_by_level = {
    "easy": ["кот", "собака", "яблоко", "молоко", "солнце"],
    "medium": ["банан", "школа", "друг", "окно", "жёлтый"],
    "hard": ["технология", "университет", "информация", "произношение", "воображение"]
}
score = 0
difficulty = input("Выберите уровень сложности (easy, medium, hard): ")
translator = Translator()
while True:
    word = random.choice(words_by_level[difficulty])
    print(word)
    print('Говори:')
    recording = sd.rec( 
        int(duration * sample_rate), # длительность записи в сэмплах
        samplerate=sample_rate,      # частота дискретизации
        channels=1,                  # 1 — это моно
        dtype="int16")               # формат аудиоданных
    sd.wait()  # ждём завершения записи
    wav.write("output.wav", sample_rate, recording)
    print("Запись завершена, теперь распознаём...")
    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile("output.wav") as source:
            audio = recognizer.record(source)
        recognized = recognizer.recognize_google(audio, language="en-US").lower()
        translation = translator.translate(word, src="ru", dest="en").text.lower()
        print(f"Ты сказал: {recognized}")
        print(f"Ожидалось: {translation}")
        if recognized == translation:
            print("Верно!")
            score += 1
        else:
            print("Неверно.")
    except sr.UnknownValueError:
        print("Не удалось распознать речь.")
    except sr.RequestError as e:
        print(f"Ошибка сервиса: {e}")
