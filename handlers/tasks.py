from aiogram import types
from aiogram.dispatcher import Dispatcher
import json
import random

def register_task_handlers(dp: Dispatcher):
    @dp.message_handler(commands=['task'])
    async def send_task(message: types.Message):
        with open('data/tasks.json', encoding='utf-8') as f:
            tasks = json.load(f)
        task = random.choice(tasks)

        keyboard = types.InlineKeyboardMarkup()
        for option in task['options']:
            keyboard.add(types.InlineKeyboardButton(
                text=option,
                callback_data=f"task_{option}___{task['answer']}"
            ))

        await message.answer(task['task'], reply_markup=keyboard)

    @dp.callback_query_handler(lambda c: c.data and c.data.startswith('task_'))
    async def process_task_answer(callback_query: types.CallbackQuery):
        data = callback_query.data[5:] 
        selected, correct = data.split("___")

        if selected == correct:
            text = "✅ Правильно! Молодец!"
        else:
            text = f"❌ Неправильно! Правильный ответ: {correct}"

        await callback_query.answer(text, show_alert=True)
