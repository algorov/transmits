import vk_api
import userHandler
import TCPClient
import sys
from vk_api.longpoll import VkLongPoll

token = "vk1.a.5xSRIXg8uyq6ICFOJFJJHJ8Y7bZPSSZZEAIrV6-BytPnfZs1GDT4awdLccRunivkoMKP-eHiIEZRgXHHP4xlWuRvzZ0kpozd83CfvrflxWldpbQn_nRgEpcl_d22P8D5semFaFu8q-Fxx3YJZnde95BSk5JMQFnzd-3IKA8xo7pnOkaVn-HrMByFNuKq5DVV4gIFJ8F9q4sReLOXXm1adA"

vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()

# Основной цикл бота
longpoll = VkLongPoll(vk_session)
for event in longpoll.listen():
    userHandler.handleEvent(event, vk)