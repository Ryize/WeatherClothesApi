# WeatherClothesApi
Проект по подбору одежды с учетом погоды в выбранном городе. Запрос и ответ были представлены через API (от DjangoRestFramework).

## Использованные технологии: 


![](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

## Развернуть проект локально:

> Установите Python (если он не установлен, рекомендуется Python 3.10)<br>
> [Download Python3](https://www.python.org/downloads/)

Клонируйте репозиторий и перейдите в папку с проектом:
```
git clone https://github.com/Ryize/WeatherClothesApi.git
cd WeatherClothesApi
```

Установите зависимости:
```
pip3 install -r requirements.txt
```

Рекомендуем изменить SECRET_KEY (для этого откройте файл RobinPage/settings.py):
```
SECRET_KEY = "Ваш SECRET_KEY"
```

Выполните миграции:
```
python3 manage.py migrate
```

Запустите сервер:
```
python3 manage.py runserver
```
