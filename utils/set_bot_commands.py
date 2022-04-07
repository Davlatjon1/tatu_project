from aiogram import types

from data import config


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Перезагрузить бота"),
        types.BotCommand("all_items", "Вывести все товары"),
        types.BotCommand("help", "Помощь"),
        types.BotCommand("search", "Поиск")
    ])
