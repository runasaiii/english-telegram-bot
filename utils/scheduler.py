import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import json
import random
from aiogram import types 

scheduler = AsyncIOScheduler()

from utils.database import was_sent, mark_as_sent

async def send_word_of_the_day(bot, chat_id):
    with open('data/words.json', encoding='utf-8') as f:
        words = json.load(f)

    random.shuffle(words)
    for word in words:
        key = word['en']  
        if not was_sent('word', key):
            mark_as_sent('word', key)
            text = (
                f"📘 Word of the Day:\n\n"
                f"<b>{word['en']}</b> {word['tr']}\n"
                f"{word['ru']}\n"
            )

            await bot.send_message(chat_id, text, parse_mode='HTML')
            return

    await bot.send_message(chat_id, "✅ Все слова уже были! Добавь новые в базу.")


async def send_task(bot, chat_id):
    with open('data/tasks.json', encoding='utf-8') as f:
        tasks = json.load(f)
    task = random.choice(tasks)

    keyboard = types.InlineKeyboardMarkup()
    for option in task['options']:
        keyboard.add(types.InlineKeyboardButton(
            text=option,
            callback_data=f"task_{option}___{task['answer']}"
        ))

    await bot.send_message(chat_id, task['task'], reply_markup=keyboard)


async def send_quiz(bot, chat_id):
    with open('data/grammar_tests.json', encoding='utf-8') as f:
        tests = json.load(f)
    test = random.choice(tests)

    keyboard = types.InlineKeyboardMarkup()
    for option in test['options']:
        keyboard.add(types.InlineKeyboardButton(
            text=option,
            callback_data=f"quiz_{option}___{test['answer']}"
        ))

    await bot.send_message(chat_id, test['question'], reply_markup=keyboard)


def start_scheduler(bot, chat_id):
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
    from apscheduler.triggers.interval import IntervalTrigger
    import asyncio

    scheduler = AsyncIOScheduler()
    
    scheduler.add_job(
        send_word_of_the_day,
        trigger=IntervalTrigger(seconds=60),
        args=[bot, chat_id]
    )
    scheduler.add_job(
        send_task,
        trigger=IntervalTrigger(seconds=120),
        args=[bot, chat_id]
    )
    scheduler.add_job(
        send_quiz,
        trigger=IntervalTrigger(seconds=180),
        args=[bot, chat_id]
    )
    
    scheduler.start()
    print("📅 Планировщик запущен!")
