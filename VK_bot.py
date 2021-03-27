from tokens import token, PyOwm
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import requests
import bs4
from pyowm import OWM
from pyowm.utils.config import get_default_config
from pyowm.commons.exceptions import NotFoundError

vk_session = vk_api.VkApi(token=token)
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()


def weather(place):
    config_dict = get_default_config()
    config_dict['language'] = 'ru'
    owm = OWM(PyOwm)
    mgr = owm.weather_manager()

    try:
        observation = mgr.weather_at_place(place)
        w = observation.weather
        temp = w.temperature('celsius')["temp"]
        degree_sign = u'\N{DEGREE SIGN}'
        if temp > 0:
            return f"В городе {place.title()} сейчас {w.detailed_status} \n Температура: +{round(temp)}{degree_sign}С"
        else:
            return f"В городе {place.title()} сейчас {w.detailed_status} \n Температура: {round(temp)}{degree_sign}С"


    except NotFoundError:
        return f'Не найден город: {place.title()}'


def _clean_all_tag_from_str(string_line):
    result = ""
    not_skip = True
    for i in list(string_line):
        if not_skip:
            if i == "<":
                not_skip = False
            else:
                result += i
        else:
            if i == ">":
                not_skip = True

    return result


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        text = event.text.lower()
        if text == 'привет' or text == 'хай':
            if event.from_user:

                request = requests.get("https://vk.com/id" + str(event.user_id))
                bs = bs4.BeautifulSoup(request.text, "html.parser")
                user_name = _clean_all_tag_from_str(bs.findAll("title")[0])
                your_name = user_name.split()[0]

                vk.messages.send(user_id=event.user_id, message=f'Привет-привет, {your_name}!', random_id=0)
            elif event.from_chat:
                vk.messages.send(chat_id=event.chat_id, message='Привет-Привет, ребята!', random_id=0)

        elif text[:16] == 'погода в городе ':
            if event.from_user:
                vk.messages.send(user_id=event.user_id, message=weather(text[16:]), random_id=0)
            elif event.from_chat:
                vk.messages.send(chat_id=event.chat_id, message=weather(text[16:]), random_id=0)

        else:
            pass



