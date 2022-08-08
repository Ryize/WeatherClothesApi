import json
import os

import requests
from django.conf import settings
from rest_framework import views
from rest_framework.response import Response


def get_default_clothes_template() -> dict:
    """
    Используется для получения стандартного шаблона рекомендации одежды.
    Пример своего шаблона:
    {
        1: # Это просто номер, он используется в api/v1/get_all_plan
            [
                [800, 801, 802], # Коды погодных условий (https://openweathermap.org/weather-conditions)
                '25', # Минимальная текущая температура
                '50',  # Максимальная текущая температура
                'Майка, шорты, сандали. На улице тепло)' # Сообщение с рекомендацией
            ]
    }
    """
    how_to_dress = {
        1: [[800, 801, 802], '25', '50', 'Майка, шорты, сандали. На улице тепло)'],
        2: [[803, 804], '25', '35', 'Майка, шорты, сандали. На всякий случай возьмите кофту, на улице облачно)'],
        3: [[800, 801, 802, 803, 804], '10', '25', 'Футболка, кофта, штаны. На улице прохладно'],
        4: [[300, 301, 302, 310, 311, 312, 313, 314, 321, 500, 501, 502, 503, 511, 520, 521, 522, 531], '0', '40',
            'Футболка, кофта, штаны. На улице мокро, и грязно белые кроссовки не вариант!'],
        5: [[200, 201, 210, 211, 221, 230, 231], '0', '40',
            'Футболка с длинным рукавом, куртка, штаны. На улице гроза, сильный ветер. Лучше отсидеться дома...'],
        6: [[600, 601, 602, 611, 612, 613, 615, 616, 620, 621, 622], '-10', '0',
            'Футболка с длинным рукавом, кофта, куртка, тёплая обувь. На улице валит снег, если не хотите стать Дед Морозом - оденьтесь потеплее)'],
        7: [[701, 711, 721, 731, 741, 751, 761, 771], '0', '40',
            'Футболка, кофта, штаны. На улице туман, сыро, слякотно. Лучше одеться теплее!'],
        8: [[600, 601, 602, 611, 612, 613, 615, 616, 620, 621, 622], '-30', '-11',
            'Максимально тёплая одежда, на улице новый ледниковый период!!!'],
        9: [[800], '-30', '-11',
            'Максимально тёплая одежда, на улице новый ледниковый период!!!'],
    }
    return how_to_dress


def get_clothes_plan() -> dict:
    """
    Используется для получения плана одежды (стандартного или заданного в settings.py с помощью CUSTOM_CLOTHES_TEMPLATE)
    """
    try:
        how_to_dress = settings.CUSTOM_CLOTHES_TEMPLATE
    except AttributeError:
        how_to_dress = get_default_clothes_template()
    return how_to_dress


class ClothesPlanView(views.APIView):
    """
    Класс для получения рекомендации по одежде.
    Вы отправляете название города на английскуом языке и в ответ получаете словарь с данными.

    Запрос: curl api/v1/Moscow
    Ответ:
    {
        "clothes_plan": "Майка, шорты, сандали. На всякий случай возьмите кофту, на улице облачно)",
        "description": "Пасмурно",
        "temp_now": 31.79,
        "temp_min": 31.29,
        "temp_max": 32.24
    }
    """

    def get(self, request, location: str):
        APPID = settings.OPEN_WEATHER_MAP_APPID
        response = requests.get("http://api.openweathermap.org/data/2.5/weather",
                                params={'q': location, 'units': 'metric', 'lang': 'ru',
                                        'APPID': APPID})
        data = json.loads(response.text)
        try:
            result = self._get_result_dict(*self._get_clothes_plan(data))
        except KeyError:
            result = {
                'status': 404,
                'description': 'Город с таким названием не найден!',
            }
            return Response(result, result['status'])

        return Response(result)

    def _get_clothes_plan(self, data: dict) -> tuple:
        """ Получения плана одежды в определённом городе """
        how_to_dress = get_clothes_plan()
        conditions_id = data['weather'][0]['id']
        description = data['weather'][0]['description']
        temp_now = data['main']['temp']
        temp_min = data['main']['temp_min']
        temp_max = data['main']['temp_max']
        for dress in how_to_dress.values():
            if conditions_id in dress[0] and int(dress[1]) <= temp_now <= int(dress[2]):
                clothes_plan = dress[3]
                break
        else:
            clothes_plan = 'На улице непонятная жесть, рекомендуем вам остаться дома!'
        return clothes_plan, description, temp_max, temp_min, temp_now

    def _get_result_dict(self, clothes_plan: str, description: str, temp_max: int, temp_min: int,
                         temp_now: int) -> dict:
        """ Получение словаря для ответа клиенту """
        result = {
            'clothes_plan': clothes_plan,
            'description': description.capitalize(),
            'temp_now': temp_now,
            'temp_min': temp_min,
            'temp_max': temp_max,
        }
        return result


class GetPlanWeatherIDView(views.APIView):
    """
    Класс для получения плана на указанную погоду (погода передаётся по id - https://openweathermap.org/weather-conditions).
    Вы отправляете название города на английскуом языке и в ответ получаете словарь с данными.

    Запрос: curl api/v1/get_plan/800
    Ответ:
    {
        "id": 800,
        "status": 200,
        "clothes_plan": "Майка, шорты, сандали. На улице тепло)",
        "temp_min": "25",
        "temp_max": "50"
    }
    """

    def get(self, request, pk: int):
        how_to_dress = get_clothes_plan()
        for dress in how_to_dress.values():
            if pk in dress[0]:
                clothes_plan = {
                    'id': pk,
                    'status': 200,
                    'clothes_plan': dress[3],
                    'temp_min': dress[1],
                    'temp_max': dress[2],
                }
                break
        else:
            clothes_plan = {
                'id': pk,
                'status': 404,
                'description': 'Мы не нашли план для такой погоды!'
            }
        return Response(clothes_plan, status=clothes_plan['status'])


class GetAllWeatherPlanView(views.APIView):
    """
    Класс для получения списка всех планов одежды.

    Запрос: curl api/v1/get_all_plan/
    Ответ:
    {
        "1": {
            "id": [800, 801, 802],
            "clothes_plan": "Майка, шорты, сандали. На улице тепло)",
            "temp_min": "25",
            "temp_max": "50"
        },
        "2": {
            "id": [800],
            "clothes_plan": "Максимально тёплая одежда, на улице новый ледниковый период!!!",
            "temp_min": "-30",
            "temp_max": "-11"
        }
    }
    """

    def get(self, request):
        all_plan = {}
        for key, dress in get_clothes_plan().items():
            all_plan[key] = {
                'id': dress[0],
                'clothes_plan': dress[3],
                'temp_min': dress[1],
                'temp_max': dress[2],
            }
        return Response(all_plan)


class GetCitiesListView(views.APIView):
    """
    Используется для получения списка городов и информации о них.
    Название городов можно использоваться для получения рекомендации по одежде (api/v1/<НазваниеГорода>)

    Пример ответа (для одного города, на самом деле их очень много):
    [
      {
        "id": 14256,
        "coord": {
          "lon": 48.570728,
          "lat": 34.790878
        },
        "country": "IR",
        "geoname": {
          "cl": "P",
          "code": "PPL",
          "parent": 132142
        },
        "langs": [
          {
            "de": "Azad Shahr"
          },
          {
            "fa": "آزادشهر"
          }
        ],
        "name": "Azadshahr",
        "stat": {
          "level": 1.0,
          "population": 514102
        },
        "stations": [
          {
            "id": 7030,
            "dist": 9,
            "kf": 1
          }
        ],
        "zoom": 10
      },
       ...
    ]
    """

    def get(self, request):
        with open('Api/static/current.city.list.json', 'r') as file:
            data = json.loads(file.read())
        return Response(data)
