from aiogram import types
from aiogram.dispatcher import Dispatcher
import json
import random

def register_word_handlers(dp: Dispatcher):
    @dp.message_handler(commands=['word'])
    async def send_word(message: types.Message):
        with open('data/words.json', encoding='utf-8') as f:
            words = json.load(f)
        word = random.choice(words)
        text = f"📘 Word of the Day:\n\n<b>{word['word']}</b> {word['transcription']}\n{word['translation']}\n\n🔹 Example:\n{word['example']}"
        await message.answer(text, parse_mode='HTML')
