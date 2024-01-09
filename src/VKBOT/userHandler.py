import vk_api
from vk_api.longpoll import VkEventType, VkLongPoll
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import datetime

MAX_INACTIVE_TIME = 240
#stage 0 - объяснение, кнопка начать -> 1
#stage 1 - ввод tgid -> 2
#stage 2 - ввод сообщения -> 3
#stage 3 - подтверждение отправки, кнопка для изменения id, кнопка для изменения сообщ, кнопка отправить -> 4 || -> 5
#stage 4 - изменение tgid -> 3
#stage 5 - изменение message -> 3

stage0_keyboard = VkKeyboard(one_time=True)
stage0_keyboard.add_button("Начать", color=VkKeyboardColor.POSITIVE)

stage3_keyboard = VkKeyboard(one_time = True)
stage3_keyboard.add_button("Изменить Id", color=VkKeyboardColor.POSITIVE)
stage3_keyboard.add_button("Изменить Сообщение", color=VkKeyboardColor.POSITIVE)
stage3_keyboard.add_button("Отправить", color=VkKeyboardColor.NEGATIVE)

class User:
    def __init__(self, vk, user_id) -> None:
        self.user_id = user_id
        self.current_stage = 0
        self.vk = vk
        self.reciever_id = -1
        self.msg_to_send = ""
        self.last_active = datetime.datetime.now()


    def require_delete(self):
        now = datetime.datetime.now()
        return (now-self.last_active).total_seconds() >= MAX_INACTIVE_TIME


    def handle(self, event):
        self.last_active = datetime.datetime.now()
        if self.current_stage == 0:
            if(event.text == 'Начать'):
                user_id = event.user_id
                self.vk.messages.send(
                        user_id=user_id,
                        message="Отлично! Введите Telegram Id получателя",
                        random_id = 0
                )
                self.current_stage = 1
            else:
                user_id = event.user_id
                self.vk.messages.send(
                        user_id=user_id,
                        message="Для отправки сообщения вам необходимо будет ввести Telegram Id получателя и текст сообщения. Нажмите Начать для продолжения",
                        keyboard=stage0_keyboard.get_keyboard(),
                        random_id = 0
                )
        elif self.current_stage == 1:
            self.reciever_id = event.text
            user_id = event.user_id
            self.vk.messages.send(
                    user_id=user_id,
                    message="Вы ввели Tegegram Id:" + self.reciever_id + ". Теперь введите сообщение",
                    random_id = 0
            )
            self.current_stage = 2
        elif self.current_stage == 2:
            self.msg_to_send = event.text
            user_id = event.user_id
            self.vk.messages.send(
                    user_id=user_id,
                    message="Вы ввели Сообщение:" + self.msg_to_send + ". Теперь вы можете изменить адрес получателя или текст сообщения. Если всё верно нажмите кнопку Отправить",
                    keyboard=stage3_keyboard.get_keyboard(),
                    random_id = 0
            )
            self.current_stage = 3
        elif self.current_stage == 3:
            responce = event.text
            if event.text == "Изменить Id":
                user_id = event.user_id
                self.vk.messages.send(
                        user_id=user_id,
                        message="Введите новый Id получателя",
                        random_id = 0
                )
                self.current_stage = 4
            elif event.text == "Изменить Сообщение":
                user_id = event.user_id
                self.vk.messages.send(
                        user_id=user_id,
                        message="Введите сообщение заново",
                        random_id = 0
                )
                self.current_stage = 5
            elif event.text == "Отправить":
                user_id = event.user_id
                self.vk.messages.send(
                        user_id=user_id,
                        message="Сообщение отправлено. Для отправки нового сообщения вам необходимо будет ввести Telegram Id получателя и текст сообщения. Нажмите Начать для продолжения",
                        keyboard=stage0_keyboard.get_keyboard(),
                        random_id = 0
                )
            else:
                user_id = event.user_id
                self.vk.messages.send(
                    user_id=user_id,
                    message="Команда не распознана. Вы ввели Сообщение:" + self.msg_to_send + " для получателя с id:" + self.reciever_id + ". Теперь вы можете изменить адрес получателя или текст сообщения. Если всё верно нажмите кнопку Отправить",
                    keyboard=stage3_keyboard.get_keyboard(),
                    random_id = 0
                )
        elif self.current_stage == 4:
            self.reciever_id = event.text
            user_id = event.user_id
            self.vk.messages.send(
                    user_id=user_id,
                    message="Вы ввели Сообщение:" + self.msg_to_send + " для получателя с id:" + self.reciever_id + ". Теперь вы можете изменить адрес получателя или текст сообщения. Если всё верно нажмите кнопку Отправить",
                    keyboard=stage3_keyboard.get_keyboard(),
                    random_id = 0
            )
            self.current_stage = 3
        elif self.current_stage == 5:
            self.msg_to_send = event.text
            user_id = event.user_id
            self.vk.messages.send(
                    user_id=user_id,
                    message="Вы ввели Сообщение:" + self.msg_to_send + " для получателя с id:" + self.reciever_id + ". Теперь вы можете изменить адрес получателя или текст сообщения. Если всё верно нажмите кнопку Отправить",
                    keyboard=stage3_keyboard.get_keyboard(),
                    random_id = 0
            )
            self.current_stage = 3

usersDict = {}
def handleEvent(event, vk):
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        for user in usersDict.keys():
            if usersDict[user].require_delete():
                del usersDict[user]

        user_id = event.user_id

        if not(user_id in usersDict):
            user = User(vk, user_id)
            usersDict[user_id] = user
        usersDict[user_id].handle(event)
    