import queue

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv
import os
import json


class Bot:
    def __init__(self, in_queue: queue.Queue, out_queue: queue.Queue):
        self.application = None
        self.bot_token = None
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.load_environment()
        self.create_application()

    def load_environment(self):
        load_dotenv()
        self.bot_token = os.getenv('BOT_TOKEN')

    def create_application(self):
        self.application = Application.builder().token(self.bot_token).build()
        self.register_handlers()

    def start(self):
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

    def build_post(self, data: list, id: int) -> None:
        somee = {
            "data": {
                "sender": id,
                "recipient": data[0],
                "message": data[1]
            }
        }
        json_format = json.dumps(somee)
        self.out_queue.put(json_format)

    def register_handlers(self):
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("post", self.post_command))
        self.application.add_handler(CommandHandler("get", self.get_command))

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user = update.effective_user
        await update.message.reply_html(
            rf"Hi {user.mention_html()}!",
            reply_markup=ForceReply(selective=True),
        )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("Help!")

    async def get_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not self.in_queue.empty():
            while not self.in_queue.empty():
                json_format = self.in_queue.get()
                data = json.loads(json_format)
                print("HEHEHEHEHEHEHEHE")
                print(data)
        else:
            await update.message.reply_text("Пока что нет новых сообщений!")

    async def post_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(
            "Отправьте данные по одному сообщению: ID в ВК и само сообщение. Чтобы закончить - /done")

        data = []
        step = 0

        async def process_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            nonlocal data, step

            if update.message.text.lower() == '/done':
                data = []
                step = 0
                self.application.remove_handler(txt_handler)
                self.application.remove_handler(cmd_handler)
            else:
                data.append(update.message.text)

                step += 1
                if step == 2:
                    self.build_post(data, update.message.from_user.id)
                    data = []
                    step = 0
                    self.application.remove_handler(txt_handler)
                    self.application.remove_handler(cmd_handler)
                    await update.message.reply_text("Если запрос валидный, то всё будет классно!")

        txt_handler = MessageHandler(filters.TEXT, process_data)
        cmd_handler = CommandHandler('done', process_data)
        self.application.add_handler(txt_handler)
        self.application.add_handler(cmd_handler)


if __name__ == '__main__':
    bot = Bot()
    bot.start()
