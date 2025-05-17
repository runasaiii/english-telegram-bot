from aiogram import types
from aiogram.dispatcher import Dispatcher
import json
import random

def register_quiz_handlers(dp: Dispatcher):
    @dp.message_handler(commands=['quiz'])
    async def send_quiz(message: types.Message):
        with open('data/grammar_tests.json', encoding='utf-8') as f:
            tests = json.load(f)
        test = random.choice(tests)

        keyboard = types.InlineKeyboardMarkup()
        for option in test['options']:
            keyboard.add(types.InlineKeyboardButton(
                text=option,
                callback_data=f"quiz_{option}___{test['answer']}"
            ))

        await message.answer(test['question'], reply_markup=keyboard)

    @dp.callback_query_handler(lambda c: c.data and c.data.startswith('quiz_'))
    async def process_quiz_answer(callback_query: types.CallbackQuery):
        data = callback_query.data[5:]  
        selected, correct = data.split("___")

        if selected == correct:
            text = "✅ Правильно! Ты молодец :3"
        else:
            text = f"❌ Неправильно! Правильный ответ: {correct}"

        await callback_query.answer(text, show_alert=True)
