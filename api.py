# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с JSON и логами.
import json
import logging
from datetime import time
from models import Order
from heapq import heappush, heappop
# Импортируем подмодули Flask для запуска веб-сервиса.


from models import User 


logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {}

recipes = {'Борщ': time(0, 2, 40), 'Грибной суп':  time(0, 2, 27),
           'Рис с сухофруктами и курица в томатном соусе': time(0, 3, 20),
           'Яичная лапша с говядиной в соусе': time(0, 4, 56),
           'Кsарбонара': time(0, 5, 20), 'Бефстроганов': time(0, 3, 53),
           'Мясная котлета с картофелем айдахо и томатным соусом': time(0, 8, 27)}
current_orders = []
order_heap = []
orders = []
order_id = 0
cook_time = time(0, 7, 0)

empl_list = {'Cook1': True, 'Cook2': True, 'Cook3': True}

roles = {'Клиент': 0, 'Повар': 1, 'Менеджер': 2}

# Задаем параметры приложения Flask.
from flask import Flask, request

app = Flask(__name__)
@app.route("/", methods=['POST'])

def main():
# Функция получает тело запроса и возвращает ответ.
    logging.info('Request: %r', request.json)

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }

    handle_dialog(request.json, response)

    logging.info('Response: %r', response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )

# Функция для непосредственной обработки диалога.
def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        res['response']['text'] = 'Добро пожаловать! Можете представиться?'
        sessionStorage[user_id] = {
            'suggests': [
                "Клиент",
                "Повар",
                "Менеджер",
            ]
        }
        # users.append(User(user_id, 1, 1))
        # res['response']['buttons'] = get_suggests(user_id)
        return 

    # Обрабатываем ответ пользователя.
    tokens = req['request']['original_utterance'].split()
    user = get_user(user_id)
    if user.role == 1 :
        if tokens and tokens[0].lower() in [
            'сделал',
            'доделал',
            'все',
            'закончил',
            'готово'
        ]:
            res['response']['text'] = 'Молодец!'
            for order in allOrders: 
                if (order.cookerId == user_id and order.status == 'in_progress') :
                    order.status = 'finished'
                    break
            user.status = 1
            return 
        if req['request']['original_utterance'].isnumeric() :
            res['response']['text'] = 'Хорошо, мы уведомим об этом менеджера. Надеюсь клиент не останется голодным('
            return
        send_message(req['request']['original_utterance'])
    if user.role == 0 :
        if tokens and tokens[0] == 'Приготовь':
        if (len(tokens) == 1):
            res['response']['text'] = 'Хз что готовить'
            return
        recipe = ' '.join(tokens[1:])
        
        if (recipes.get(recipe) != None):
            item = recipes.get(recipe)
            order = Order(recipe, time(0, 6-item.minute, 60-item.second))
            heappush(order_heap, order)
            res['response']['text'] = 'Заказ добавлен в очередь!'



def get_user(id) :
    for user in users :
        if (user.userId == id):
            return user
    # return filter(lambda user: user.userId == id, users)

def send_message(text)
    print(text)

def get_suggests(user_id):
    session = sessionStorage[user_id]

    # Выбираем две первые подсказки из массива.
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]

    # Убираем первую подсказку, чтобы подсказки менялись каждый раз.
    session['suggests'] = session['suggests'][1:]
    sessionStorage[user_id] = session

    # Если осталась только одна подсказка, предлагаем подсказку
    # со ссылкой на Яндекс.Маркет.
    if len(suggests) < 2:
        suggests.append({
            "title": "Ладно",
            "url": "https://market.yandex.ru/search?text=слон",
            "hide": True
        })

    return suggests

