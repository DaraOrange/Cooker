# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с JSON и логами.
import json
import logging
from datetime import time

# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request
app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {}

recipes = {'Борщ': time(0, 2, 40), 'Грибной суп':  time(0, 2, 27),
           'Рис с сухофруктами и курица в томатном соусе': time(0, 3, 20),
           'Яичная лапша с говядиной в соусе': time(0, 4, 56),
           'Карбонара': time(0, 5, 20), 'Бефстроганов': time(0, 3, 53),
           'Мясная котлета с картофелем айдахо и томатным соусом': time(0, 8, 27)
current_orders = []

empl_list = {'Cook1': true, 'Cook2': true, 'Cook3': true}

# Задаем параметры приложения Flask.
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
        res['response']['text'] = 'Добро пожаловать! Уверена, вы найдете то, что понравится вашему желудку!'
        #TODO: Menu for customers
        # res['response']['buttons'] = get_suggests(user_id)
        return

    # Обрабатываем ответ пользователя.
    if req['request']['original_utterance'].size() != 0 :
        uttr = req['request']['original_utterance']
        if uttr.size() != 0 :
            for recipe in recipes:
                if (recipe[0] == uttr)
                    order = Order(recipe, 7*60, recipe[1].hour*3600 +
                                 recipe[1].minute*60 + recipe[1]seconds, request.args.get("time") + recipe[1])
                    

def add_order(order, meal):
        heappush(order.PlanLeadTime - (order.StartTime + food.PlanLeadTime), order.id)


def manage_order():
    while (current_orders.size() != 0):
        cooker = get_free_cooker()
        cooker.status = 0
        {order, food} = heappop(current_orders)
        fullorder = FullOrder(order.id, food.id, cooker.id, "in_progress", order.PlanLeadTime, 
                              order.StartTime, order.StartTime + food.PlanLeadTime);
def add_order_with_additional_time(fullorder, current_time, additinal_time)
    updatedOrder = FullOrder(fullorder.orderId, fullorder.foodId, fullorder.cookerId, fullorder.status,
                             fullorder.LeadTime, fullorder.StartTime, current_time + additinal_time)

