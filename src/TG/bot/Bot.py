import os
import queue
import json

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv


class Bot:
    def __init__(self, in_msgs: dict, out_queue: queue.Queue):
        self.application = None
        self.bot_token = None
        self.in_msgs = in_msgs
        self.out_queue = out_queue

        self.load_environment()
        self.create_application()

    def load_environment(self) -> None:
        load_dotenv()
        self.bot_token = os.getenv('BOT_TOKEN')

    def create_application(self) -> None:
        self.application = Application.builder().token(self.bot_token).build()
        self.register_handlers()

    def start(self) -> None:
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

    def validate_data(self, data: list) -> bool:
        if data[0].isdigit() and 0 < len(data[0]) <= 20 and 0 < len(data[1]) <= 512:
            return True
        else:
            return False

    def build_json(self, nickname: str, data: list) -> str:
        this = {
            "data": {
                "sender": nickname,
                "recipient": data[0],
                "msg": data[1]
            }
        }

        return json.dumps(this) + "\n"

    def register_handlers(self) -> None:
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("post", self.post_command))
        self.application.add_handler(CommandHandler("get", self.get_command))

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user = update.effective_user
        await update.message.reply_html(rf"Hi {user.mention_html()}! 🖖🏻 Чтобы узнать подробнее, пошлите /help")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(
            "❓Чтобы отправить сообщение: /post\n"
            "❓Чтобы проверить почту: /get"
        )

    async def get_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        tg_id = str(update.message.from_user.id)
        msgs = []

        print(f'[GET] from {tg_id}:\n* MSGS DICT: {self.in_msgs}')

        if tg_id in self.in_msgs:
            await update.message.reply_text("Для вас есть кое-что! ✅")

            msgs = [msg for date, msg in self.in_msgs[tg_id].items()]
            for msg in msgs:
                json_format = msg
                data = json.loads(json_format)
                await update.message.reply_markdown(
                    f'*От {data.get("data").get("sender")}:*\n {data.get("data").get("msg")}')

            del self.in_msgs[tg_id]
        else:
            await update.message.reply_text("📌 Для вас пока нет ничего нового!")

    async def post_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_markdown(
            "Отправьте данные по одному сообщению: \n"
            "1️⃣ *ID получателя в VK*\n"
            "2️⃣ *Cообщение*\n"
            "Вернуться назад: /back")

        data = []
        step = 0

        async def process_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            nonlocal data, step
            if update.message.text.lower() == '/back':
                data = []
                step = 0
                self.application.remove_handler(txt_handler)
                self.application.remove_handler(cmd_handler)
                await update.message.reply_text("🔙 Отмена!")
            else:
                data.append(update.message.text)
                step += 1
                if step == 2:
                    if self.validate_data(data):
                        self.out_queue.put(self.build_json(update.message.from_user.full_name, data))
                        await update.message.reply_text("Сообщение отправлено! 🙄")
                    else:
                        await update.message.reply_text("Некорректные данные! 🤬")

                    data = []
                    step = 0
                    self.application.remove_handler(txt_handler)
                    self.application.remove_handler(cmd_handler)

        txt_handler = MessageHandler(filters.TEXT, process_data)
        cmd_handler = CommandHandler('back', process_data)
        self.application.add_handler(txt_handler)
        self.application.add_handler(cmd_handler)


if __name__ == '__main__':
    bot = Bot()
    bot.start()
