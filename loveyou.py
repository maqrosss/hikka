import random
from telethon import types
from .. import loader, utils

lol = ["я типя тожи", "ты педик?", 'асуууууууууууу', 'ичо', 'пиздец', 'явахуе', 'так ей и сказал?', 'флоресто фуре', 'попа пиписька кашака', 'я клик', 'БЛЯТЬ МЕНЯ ВЗЛОМАЛИ', 'ичо блять чмо', 'не бань пршу', 'даймне пососать']
msgsl = ["ку", 're', 'dev', 'динахуй','иди нахуй','дон','я дон', 'клик', 'я тебя люблю', 'я типя люблю', 'я тебя любл', 'чо как', 'как дела', 'дарова', 'дорова', 'педик', 'сам такой', ]

@loader.tds
class MegaMozgMod(loader.Module):
    strings = {
        "name": "DEVbrain",
        "pref": "<b>[DEVbrain]</b> ",
        "need_arg": "{}Нужен аргумент",
        "status": "{}{}",
        "on": "{}готоф трахат",
        "off": "{}ни гатоф трахат",
    }
    _db_name = "DEVtheBest"

    async def client_ready(self, _, db):
        self.db = db

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

    async def mozgcmd(self, m: types.Message):
        ".dev <on/off/...> - Переключить режим флоресто в чате"
        args = utils.get_args_raw(m)
        if not m.chat:
            return
        chat = m.chat.id
        if self.str2bool(args):
            chats: list = self.db.get(self._db_name, "chats", [])
            chats.append(chat)
            chats = list(set(chats))
            self.db.set(self._db_name, "chats", chats)
            return await utils.answer(
                m, self.strings("on").format(self.strings("pref"))
            )
        chats: list = self.db.get(self._db_name, "chats", [])
        try:
            chats.remove(chat)
        except:
            pass
        chats = list(set(chats))
        self.db.set(self._db_name, "chats", chats)
        return await utils.answer(m, self.strings("off").format(self.strings("pref")))

    async def mozgchancecmd(self, m: types.Message):
        ".devc <int> - Устанвоить шанс 1 к N.\n0 - всегда отвечать"
        args: str = utils.get_args_raw(m)
        if args.isdigit():
            self.db.set(self._db_name, "chance", int(args))
            return await utils.answer(
                m, self.strings("status").format(self.strings("pref"), args)
            )
        return await utils.answer(
            m, self.strings("need_arg").format(self.strings("pref"))
        )

    async def watcher(self, m: types.Message):
        if not isinstance(m, types.Message):
            return
        if m.sender_id == (await m.client.get_me()).id or not m.chat:
            return
        if m.chat.id not in self.db.get(self._db_name, "chats", []):
            return
        for phrase in msgsl:
            if phrase.lower() in m.text.lower():
                await m.reply(random.choice(lol))
                return

