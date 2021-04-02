from tokens import token, PyOwm
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import requests, httplib2
from bs4 import BeautifulSoup, SoupStrainer
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



def get_fanfiction(fandom):
    url = "https://ficbook.net/fanfiction/%20/" + fandom.replace(" ", "_")
    fanfictions = []
    names = []
    http = httplib2.Http()
    status, response = http.request(url)
    for link in BeautifulSoup(response, 'html.parser', parse_only=SoupStrainer('a')):
        if link.has_attr('href'):
            if "/readfic/" in link['href'] and not "premium" in link['href']:
                fanfictions.append("http://ficbook.net" + link['href'])
    fanfictions = fanfictions[:3]

    for f in fanfictions:
        r = requests.get(f)
        soup = BeautifulSoup(r.text, 'lxml')
        name = soup.find_all('h1')
        names.append([elem.string for elem in name])
    it = 0
    result = []
    for i in names:
        for j in i:
            result.append(fanfictions[it] + " --> " + j + "\n")
            it += 1
    return result


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

        request = requests.get("https://vk.com/id" + str(event.user_id))
        bs = BeautifulSoup(request.text, "html.parser")
        user_name = _clean_all_tag_from_str(bs.findAll("title")[0])
        your_name = user_name.split()[0]

        if text[:16] == 'погода в городе ':
            if event.from_user:
                vk.messages.send(user_id=event.user_id, message=weather(text[16:]), random_id=0)
            elif event.from_chat:
                vk.messages.send(chat_id=event.chat_id, message=weather(text[16:]), random_id=0)

        elif text[:11] == 'фанфики по ':
            if event.from_user:
                vk.messages.send(user_id=event.user_id, message=get_fanfiction(text[11:].lower()), random_id=0)
            elif event.from_chat:
                vk.messages.send(user_id=event.chat_id, message=get_fanfiction(text[11:].lower()), random_id=0)

        elif text == "пока" or text == "бай":
            if event.from_user:
                vk.messages.send(user_id=event.user_id, message=f"Пока-пока, {your_name}!", random_id=0)
            elif event.from_chat:
                vk.messages.send(user_id=event.chat_id, message="Пока-пока, ребята!", random_id=0)

        elif text == 'привет' or text == 'хай':
            if event.from_user:
                vk.messages.send(user_id=event.user_id, message=f'Привет-привет, {your_name}!', random_id=0)
            elif event.from_chat:
                vk.messages.send(chat_id=event.chat_id, message='Привет-Привет, ребята!', random_id=0)

        else:
            if event.from_user:
                vk.messages.send(user_id=event.user_id, message='Я Вас не понимаю((...', random_id=0)
            elif event.from_chat:
                vk.messages.send(chat_id=event.chat_id, message='Я вас не понимаю((...', random_id=0)
