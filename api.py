# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с JSON и логами.
import json
import logging

# Импортируем подмодули Flask для запуска веб-сервиса.
from datetime import time
from models import Order
from user import User
from heapq import heappush, heappop

logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {}

# Задаем параметры приложения Flask.

recipes = {'борщ': time(0, 2, 40), 'грибной суп':  time(0, 2, 27),
           'рис с сухофруктами и курица в томатном соусе': time(0, 3, 20),
           'яичная лапша с говядиной в соусе': time(0, 4, 56),
           'карбонара': time(0, 5, 20), 'бефстроганов': time(0, 3, 53),
               'мясная котлета с картофелем айдахо и томатным соусом': time(0, 8, 27)}
current_orders = []
order_heap = []
orders = []
users = []
order_id = 0
cook_time = time(0, 7, 0)

empl_list = {'Cook1': True, 'Cook2': True, 'Cook3': True}

roles = {'Клиент': 0, 'Повар': 1, 'Менеджер': 2}

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
        #TODO: Menu for customers
        # res['response']['buttons'] = get_suggests(user_id)
        return

    # Обрабатываем ответ пользователя.
    tokens = req['request']['original_utterance'].split()
    user = get_user(user_id)
    if tokens and tokens[0] in [
            "Клиент",
            "Повар",
            "Менеджер",
        ]:
            users.append(User(user_id, roles[tokens[0]], 1))
            res['response']['text'] = 'Очень приятно'
            return 
        
    if user.role == 1 :
        if tokens and tokens[0].lower() in [
            'сделал',
            'доделал',
            'все',
            'закончил',
            'готово'
        ]:
            res['response']['text'] = 'Молодец!'
            return 
    if tokens and tokens[0].lower() == 'приготовь':
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

# Функция возвращает две подсказки для ответа.
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
