import os
import telebot
from gtts import gTTS
import speech_recognition as sr
from moviepy import *

bot = telebot.TeleBot('...')


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Тут будет незамысловатое приветствие")

@bot.message_handler(commands=['pay'])
def handle_start(message):
    bot.send_message(message.chat.id, "Тут будут реквизиты для добровольных пожертвований в фонд компании на развитие бота и посещения разработчиками массажных салонов")

@bot.message_handler(commands=['profile'])
def handle_start(message):
    bot.send_message(message.chat.id, "Тут будет ваш профиль")

@bot.message_handler(commands=['progress'])
def handle_start(message):
    bot.send_message(message.chat.id, "Тут будет ваш прогресс")

@bot.message_handler(content_types=['voice'])
def voice_message(message):
    file_id = message.voice.file_id
    filename = 'audio.ogg'
    get_content(file_id, filename)


    try:
        text = recognize(filename)
        tts = gTTS(text=text, lang='ru')
        audio_file = 'output.mp3'
        tts.save(audio_file)

        with open(audio_file, 'rb') as audio:
           bot.send_voice(message.chat.id, voice=audio)


        os.remove(filename)
        os.remove('audio.wav')
        os.remove(audio_file)

    except sr.UnknownValueError:
        bot.reply_to(message, "Извините, не распознал текст в вашем аудио-сообщении. Пожалуйста, запишите его еще раз.")
    except sr.RequestError as e:
        bot.reply_to(message, f"Ошибка сервиса распознавания: {e}")
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")


def get_content(file_id, filename):
    file = bot.get_file(file_id)
    file_path = file.file_path
    downloaded_file = bot.download_file(file_path)
    with open(filename, 'wb') as new_file:
        new_file.write(downloaded_file)


def recognize(filename):
    audio = AudioFileClip(filename)
    audio.write_audiofile('audio.wav')

    recognizer = sr.Recognizer()
    with sr.AudioFile('audio.wav') as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data, language='ru-RU')
    return text


if __name__ == '__main__':
    bot.polling(none_stop=True)
