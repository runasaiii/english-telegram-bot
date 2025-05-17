from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN
from handlers.word import register_word_handlers
from handlers.tasks import register_task_handlers
from handlers.quiz import register_quiz_handlers
from utils.scheduler import start_scheduler

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.answer("Привет! Я бот для изучения английского ;)")

@dp.message_handler()
async def echo_handler(message: types.Message):
    await message.answer(f"Твой chat_id: {message.from_user.id}")

register_word_handlers(dp)
register_task_handlers(dp)
register_quiz_handlers(dp)

async def on_startup(dispatcher):
    chat_id = 1267658043
    start_scheduler(bot, chat_id)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
