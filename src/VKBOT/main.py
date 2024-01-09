import userHandler
import TCPClient
from vk_api import VkApi
from sys import argv
from os import getenv
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll

load_dotenv()
token = getenv('BOT_TOKEN_VK') #"vk1.a.5xSRIXg8uyq6ICFOJFJJHJ8Y7bZPSSZZEAIrV6-BytPnfZs1GDT4awdLccRunivkoMKP-eHiIEZRgXHHP4xlWuRvzZ0kpozd83CfvrflxWldpbQn_nRgEpcl_d22P8D5semFaFu8q-Fxx3YJZnde95BSk5JMQFnzd-3IKA8xo7pnOkaVn-HrMByFNuKq5DVV4gIFJ8F9q4sReLOXXm1adA"

vk_session = VkApi(token=token)
vk = vk_session.get_api()

serverAddr = argv[1]
serverPort = int(argv[2])

tcpClient = TCPClient.TCPClient()
tcpClient.connect(serverAddr, serverPort) 

def on_message_recieved(data):
    data = data['data']
    sender = data['sender']
    recipient = data['recipient']
    msg = data['msg']
    vk.messages.send(
        user_id = recipient,
        message = "Получено сообщение от " + str(sender) + "!\n" + msg,
        random_id = 0
    )
def on_send_data(data):
    tcpClient.send_data(data)

tcpClient.start_receive_thread(on_message_recieved)
userHandler.setup_sendMethod(on_send_data)

# Основной цикл бота
longpoll = VkLongPoll(vk_session)
for event in longpoll.listen():
    userHandler.handleEvent(event, vk)