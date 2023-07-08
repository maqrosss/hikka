import random
import asyncio
from telethon import types, TelegramClient
from .. import loader, utils

@loader.tds
class RollMod(loader.Module):
    strings = {
        "name": "Roll",
        "pref": "<b>[Roll]</b> ",
        "won": "Вы выиграли!",
        "try_again": "Попробуйте снова!",
    }
    _db_name = "Roll"

    async def client_ready(self, client, db):
        self.db = db
        await client.start()
        client.add_event_handler(self.watcher, types.NewMessage(incoming=True))

    @staticmethod
    def str2bool(v):
        return v.lower() in (
            "yes",
            "y",
            "ye",
            "yea",
            "true",
            "t",
            "1",
            "on",
            "enable",
            "start",
            "run",
            "go",
            "да",
        )

    async def rollcmd(self, m: types.Message):
        ".roll - Бросить кубик (случайное число от 1 до 100)"
        if not m.chat:
            return

        loading_message = await utils.answer(m, "Бросаем кубик...\n\nЗагрузка: 0%")
        await asyncio.sleep(0.5)

        for i in range(1, 11):
            await asyncio.sleep(0.1)
            loading_text = f"Загрузка: {i * 10}%"
            await loading_message.edit(loading_text)

        await asyncio.sleep(0.5)

        random_number = random.randint(1, 100)
        if random_number > 70:
            result = self.strings["won"]
        else:
            result = self.strings["try_again"]

        result_message = f"Бросаем кубик...\n\nРезультат: {random_number}\n{result}"
        await loading_message.edit(result_message)

