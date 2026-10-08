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


# Простая ASCII / emoji графика
def show_title():
    print()
    print("╔══════════════════════════════════════╗")
    print("║       🎤 ENGLISH SPEAKING GAME 🇬🇧  ║")
    print("╚══════════════════════════════════════╝")
    print()


def show_round(word):
    print("┌──────────────────────────────────────┐")
    print(f"│ 📝 Твоё слово: {word:<22} │")
    print("│ 🎙️  Произноси его на английском!    │")
    print("└──────────────────────────────────────┘")


def show_score(score):
    print(f"🏆 Текущий счёт: {score} ⭐")


show_title()

while True:
    difficulty = input(
        "🎮 Выберите уровень сложности (easy, medium, hard): "
    ).lower().strip()

    if difficulty in words_by_level:
        break

    print("❌ Такого уровня нет. Попробуй ещё раз.")


translator = Translator()
score = 0

while True:
    word = random.choice(words_by_level[difficulty])

    print()
    show_round(word)
    print("🎙️ Говори...")

    recording = sd.rec(
        int(duration * sample_rate),  # длительность записи в сэмплах
        samplerate=sample_rate,       # частота дискретизации
        channels=1,                   # 1 — это моно
        dtype="int16"                 # формат аудиоданных
    )

    sd.wait()
    wav.write("output.wav", sample_rate, recording)

    print("⏳ Запись завершена, теперь распознаём...")

    try:
        recognizer = sr.Recognizer()

        with sr.AudioFile("output.wav") as source:
            audio = recognizer.record(source)

        recognized = recognizer.recognize_google(
            audio,
            language="en-US"
        ).lower()

        translation = translator.translate(
            word,
            src="ru",
            dest="en"
        ).text.lower()

        print()
        print("┌────────────── Результат ──────────────┐")
        print(f"│ 🗣️  Ты сказал: {recognized}")
        print(f"│ 🎯 Ожидалось: {translation}")
        print("└───────────────────────────────────────┘")

        if recognized == translation:
            print("🎉 Верно! Отличное произношение!")
            score += 1
        else:
            print("❌ Неверно. Попробуй ещё раз!")

    except sr.UnknownValueError:
        print("😕 Не удалось распознать речь.")

    except sr.RequestError as e:
        print(f"⚠️ Ошибка сервиса: {e}")

    show_score(score)

    print()
    answer = input("🔄 Хочешь продолжить игру? (да/нет): ").lower().strip()

    if answer not in ("да", "д", "yes", "y"):
        print()
        print("╔══════════════════════════════════════╗")
        print("║          🏁 ИГРА ОКОНЧЕНА           ║")
        print(f"║          Твой счёт: {score} 🏆       ║")
        print("║        👋 Спасибо за игру!           ║")
        print("╚══════════════════════════════════════╝")
        break

    print()
    print("🚀 Отлично! Следующее слово...")
