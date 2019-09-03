# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с JSON и логами.
import json
import logging

# Импортируем подмодули Flask для запуска веб-сервиса.
from datetime import time
import datetime
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
start_tokens = ['приготовь', 'приготовить', 'новый заказ']
manager_id = None       
manager_message = ''        
current_user = -1;

empl_list = [True, True, True, True]

roles = {'crm': 4, 'менеджер': 0, 'повар1': 1, 'повар2': 2, 'повар3': 3}

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


def check_new_order(text, res):
    global order_id
    tokens = text.split()
    if tokens and (tokens[0].lower() in start_tokens):
        if (len(tokens) == 1):
            res['response']['text'] = 'Хз что готовить'
            return True
        recipe = ' '.join(tokens[1:])
        
        if (recipes.get(recipe) != None):
            timestamp = datetime.datetime.now().time()
            order_id += 1
            item = recipes.get(recipe)
            order = Order(order_id, recipe, time(0, 6-item.minute, 60-item.second), timestamp, "in_progress")
            heappush(order_heap, order)
            res['response']['text'] = 'Заказ {} добавлен в очередь!'.format(order_id)
            return True
    return False

def get_free_cooker():
    for i in range(1, 4):
        if empl_list[i] == 0:
            return i
    return -1

def add_task(res, cook_id):
    if len(order_heap) == 0:
        res['response']['text'] = 'Нет текущих заказов.'
        return
    cur_order = heappop(order_heap)
    empl_list[cook_id] = cur_order.orderId
    res['response']['text'] = 'Заказ {}: {} выполняет повар {}.'.format(cur_order.orderId, cur_order.orderName, cook_id)


def check_show_orders(text, res):
    if text == 'Очередь заказов':
        res['response']['text'] = ''
        timestamp = datetime.datetime.now().time()
        for item in order_heap:
            minutes = timestamp.minute-item.addTime.minute
            if minutes < 0:
                minutes += 60
            seconds = timestamp.second-item.addTime.second
            if seconds < 0:
                seconds += 60
                minutes -= 1
            res['response']['text'] += 'Блюдо: {}, время заказа: {}, время в очереди: {}, статус: {}\n'.format(item.orderName, item.addTime, time(0, minutes, seconds), item.status)
        if len(res['response']['text']) == 0:
            res['response']['text'] = 'Нет заказов в системе'
        return True
    return False


def check_end_task(text, res, cook_id):
    empl_list[cook_id] = 0
    add_task(res, cook_id)
    return True


# Функция для непосредственной обsработки диалога.
def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        res['response']['text'] = 'Добро пожаловать! Можете представиться?'
        sessionStorage[user_id] = {
            'suggests': [
                "crm",                     
                "менеджер",                     
                "повар1",               
                "повар2",       
                "повар3"
            ]
        }
        #TODO: Menu for customers
        res['response']['buttons'] = get_suggests(user_id)
        return

    # Обрабатываем ответ пользователя.
    text = req['request']['original_utterance']
    
    tokens = req['request']['original_utterance'].split()
    if tokens and text.lower() in roles.keys():
        # users.append(User(user_id, roles[tokens[0].lower()], 1))                    
        current_user = roles[tokens[0].lower()]
        if current_user >= 1 and current_user <= 3:
            if check_end_task(text, res, current_user):
                return
        res['response']['text'] = 'Поменяла пользователя'
        return 

    if check_show_orders(text, res):
        return
     
    if check_new_order(text, res):
        return
        
    # if user.role == 1 :
    #   res['response']['text'] = 'аолрал'
    #   return s
    # if tokens and text == ''
    # if tokens and text == 'не могу выполнить':        
 #      res['response']['text'] = 'назовите причину'
 #      return      
 #    if tokens and text.lower() == 'нет нужных ингредиентов':      
 #      res['response']['text'] = 'Ок буду согласовывать замену'

    res['response']['text'] = 'Вас не понял('
    return
            
def get_user(id) :
    for user in users :
        if (user.userId == id):
            return user
    return None

# Функция возвращает две подсказки для ответа.
def get_suggests(user_id):
    session = sessionStorage[user_id]

    # Выбираем две первые подсказки из массива.
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:5]
    ]
    return suggests