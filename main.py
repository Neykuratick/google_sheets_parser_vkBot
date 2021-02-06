from SheetHandler import SheetHandler
from ConnectSheet import ConnectSheet
from backend import Backend
import json
import datetime
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import vk_api

# pip3 install --user gspread
# pip3 install --user --upgrade google-api-python-client
# pip3 install --user --upgrade oauth2client

sh = SheetHandler()
ch = ConnectSheet()
bc = Backend()

# TOKEN = '8ad32e817674dece5ea1137f90a6c168bed3b643d467f785d3a50a1474d6ae2cfc1a2144684fa70a60677'  # testing
# group_id = 196530881  # testing
TOKEN = 'efa8f72bc9f5aab07245dbc8eb42f58551b1c56be06fc8ac549a92db582a9dfbd6866d44351067cd08534'  # release
group_id = 198604544  # release

"""
git add .
git commit -m "commit"
git push -u myorigin main
git push heroku main
heroku ps:scale worker=1
"""

vk = vk_api.VkApi(token=TOKEN)
vk._auth_token()
vk.get_api()
longpoll = VkBotLongPoll(vk, group_id)
FOO_MESSAGE = 'HELLO'


def get_button(label, color):
    return {
        'action': {
            'type': 'text',
            'payload': "{\"button\": \"" + "1" + "\"}",
            'label': label
        },
        'color': color
    }


# --- Keyboards ---

keyboardMain = {
    'one_time': False,
    'buttons': [
        [get_button('Ссылка', 'primary'), get_button('Сёдня пары', 'primary'),
         get_button('Завтра пары', 'primary'), get_button('Черта', 'primary')],

        [get_button('Эта неделя', 'positive'), get_button('Следующая неделя', 'positive')],
        [get_button('Клава иди в сраку', 'negative')]
    ]
}
keyboardMain = json.dumps(keyboardMain, ensure_ascii=False).encode('utf-8')
keyboardMain = str(keyboardMain.decode('utf-8'))

keyboardHide = {
    'one_time': True,
    'buttons': [
        [get_button('Убрать', 'negative')]
    ]
}
keyboardHide = json.dumps(keyboardHide, ensure_ascii=False).encode('utf-8')
keyboardHide = str(keyboardHide.decode('utf-8'))

keyboardThisWeek = {
    'one_time': False,
    'buttons': [
        [get_button('Понедельник покежь', 'primary'), get_button('Вторник покежь', 'primary'),
         get_button('Среду покежь', 'primary')],
        [get_button('Четверг покежь', 'primary'), get_button('Пятницу покежь', 'primary'),
         get_button('На главную', 'negative')]
    ]
}
keyboardThisWeek = json.dumps(keyboardThisWeek, ensure_ascii=False).encode('utf-8')
keyboardThisWeek = str(keyboardThisWeek.decode('utf-8'))

keyboardNextWeek = {
    'one_time': False,
    'buttons': [
        [get_button('Понедельник на следующей неделе покежь', 'primary'),
         get_button('Вторник на следующей неделе покежь', 'primary'),
         get_button('Среду на следующей неделе покежь', 'primary')],
        [get_button('Четверг на следующей неделе покежь', 'primary'),
         get_button('Пятницу на следующей неделе покежь', 'primary'), get_button('На главную', 'negative')]
    ]
}
keyboardNextWeek = json.dumps(keyboardNextWeek, ensure_ascii=False).encode('utf-8')
keyboardNextWeek = str(keyboardNextWeek.decode('utf-8'))


# --- Keyboards ---

def send_message(id, text):
    vk.method("messages.send", {"peer_id": id, "message": text, "random_id": 0})


def send_keyboard(id, keyboard):
    vk.method("messages.send", {"peer_id": id, "message": 'Ок', "random_id": 0, 'keyboard': keyboard})


def hahaList(str):
    list = []
    strToAppend = ''
    count = 1

    for char in str:
        if count < 3 or count > 4:
            if count > 4:
                list.append(strToAppend)
                strToAppend = ''
                count = 1
            strToAppend += char
            count += 1
        else:
            if count == 3:
                list.append(strToAppend)
                strToAppend = ''
            strToAppend += char
            count += 1

    return list


while True:
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:

                # writing to log
                current_time = datetime.datetime.now()
                now = current_time.strftime("%H:%M:%S")
                chat_id = str(event.object.peer_id)
                if chat_id == '2000000001':
                    chat_id = 'me'
                if chat_id == '232444433':
                    chat_id = 'me pm'
                with open('log.txt', 'a') as log:
                    log.write('Used. Time: ' + now + '. By: ' + chat_id + '\n')

                message = event.object.text.lower()
                id = event.object.peer_id

                if 'покежь' in message:
                    if 'понедельник' in message:
                        send_message(id, bc.byDay(0))

                    if 'вторник' in message:
                        send_message(id, bc.byDay(1))

                    if 'среду' in message:
                        send_message(id, bc.byDay(2))

                    if 'четверг' in message:
                        send_message(id, bc.byDay(3))

                    if 'пятницу' in message:
                        send_message(id, bc.byDay(4))

                # --

                if 'на следующей неделе покежь' in message:
                    if 'понедельник' in message:
                        send_message(id, bc.byDayNext(0))

                    if 'вторник' in message:
                        send_message(id, bc.byDayNext(1))

                    if 'сред' in message:
                        send_message(id, bc.byDayNext(2))

                    if 'четверг' in message:
                        send_message(id, bc.byDayNext(3))

                    if 'пятниц' in message:
                        send_message(id, bc.byDayNext(4))

                # --

                if 'ссылк' in message and not 'наебнулась' in message:
                    send_message(id,
                                 'https://docs.google.com/spreadsheets/d/1bAFmdln_FvbtKY-WMmSj_cyhH9l3ELgo/edit')
fwegwegww
                if 'пары' in message:
                    if 'сёдня' in message:
                        message = "e" + bc.AllForToday()
                        if message == "e":
                            send_message(id, "bc.tomorrowClasses()\ncёдня адыхаем")
                        else:
                            send_message(id, bc.AllForToday())
                    if 'завтра' in message:
                        message = "bc.tomorrowClasses() \n" + bc.tomorrowClasses()
                        send_message(id, message)
                    if 'понедельник' in message or 'пн' in message:
                        send_message(id, bc.byDay(0))
                    if 'вторник' in message:
                        send_message(id, bc.byDay(1))
                    if 'сред' in message or 'ср' in message:
                        send_message(id, bc.byDay(2))
                    if 'четверг' in message or 'чт' in message:
                        send_message(id, bc.byDay(3))
                    if 'пятниц' in message or 'пт' in message:
                        send_message(id, bc.byDay(4))

                if 'черт' in message:
                    week = datetime.date.today().isocalendar()[1]
                    if week % 2 == 0:
                        send_message(id, 'Сегодня смотрим над чертой')
                    if week % 2 == 1:
                        send_message(id, 'Сегодня смотрим под чертой')

                # --

                if 'эта неделя' in message:
                    send_keyboard(id, keyboardThisWeek)

                if 'следующая неделя' in message:
                    send_keyboard(id, keyboardNextWeek)

                if 'на главную' in message:
                    send_keyboard(id, keyboardMain)

                if 'покежь клаву' in message:
                    send_keyboard(id, keyboardMain)

                if 'убери клаву' in message:
                    send_keyboard(id, keyboardHide)

                if 'клава иди в сраку' in message:
                    send_keyboard(id, keyboardHide)

                # --

                if ("ссылка" in message or "ссылки" in message) and ("опять" in message):
                    send_message(id,
                                 'https://www.pythonanywhere.com/user/Neykuratick/files/home/Neykuratick/main.py?edit')

                if 'ха' in message:
                    hahasCount = 0
                    hahasList = hahaList(message)

                    for ha in hahasList:
                        if ha == 'ха' or ha == 'хх' or ha == 'ах':
                            hahasCount += 1

                    if 2 < hahasCount <= 4:
                        send_message(id, 'Смешно')

                    if 4 < hahasCount <= 7:
                        send_message(id, 'ыхвахывхывхыхвыавхавых бляяя')

                    if hahasCount > 7:
                        send_message(id, '1010101010101110101001 - НАСТОЛЬКО СИЛЬНО Я ОРУ ЫВХАЫХВАХЫВАХЫ')

                if 'скотина ты бот' in message:
                    if str(id) == '2000000002' or str(id) == '232444433' or str(id) == '2000000001':
                        send_message(id, 'прости человек, я буду стараться лучше')
                    else:
                        send_message(id, 'пашол в срачку, кожанная коробка')

                if "бля" in message or "хуй" in message or "пизд" in message:
                    send_message(id, 'ъуъ, не матерись, сука блеать')

                if "седня пары" in message or "пары седня" in message:
                    send_message(id, 'Кирилл с Мефодием старались, придумывсали букавы а ты вот так вот знчит к ним относишься, да? Напоминаю, что у нас помимо е есть еще ё!!!')

                if "heroku" in message:
                    send_message(id, 'Хуёку, блять')

                if 'за' in message and 'мат' in message and ('извини' in message or 'извени' in message or 'прости' in message or 'сорян' in message):
                    send_message(id, 'Привет, это Замат. Я прощаю тебя, но больше так не будь')

                # --

                if 'maintain' in message:
                    send_message(id,
                                 'https://www.pythonanywhere.com/user/Neykuratick/files/home/Neykuratick/log.txt?edit\n' + str(
                                     id))
    except:
        pass
