# test_case
Решение тестового задания на вакансию BackEnd-Разработчика в Коммерц Group, ТЗ в PDF файле репозитория.
 + [X] Создание базы данных используя миграции Django
 + [X] Скрипт для заполнения базы данных
 + [ ] Не совсем понял зачем Эндпоинт на который нужно отправлять список сотрудников со всей имеющейся о них информацией
 + [X] Возможность поиска сотрудников по любому полю, за исключением password, auth_token
 + [X] Возможность сортировки сотрудников по любому полю, за исключением password, auth_token
 + [X] Аутентификация для зарегестрированных пользователей
 + [X] Поиск и сортировка по любому полю доступна только для авторизованных пользователей
 + [ ] Не понял о каких остальных CRUD функциях идет речь
   + [X] Изменение пароля
   + [X] Изменение любых данных, не знаю зачем, но сделал
   
## Установка
Распаковываем репозиторий в удобной нам папке, после чего устанавливаем все необходимые пакеты командой:
``` 
pip install -r requirements.txt 
```

Устанавливаем базу данных PostgreSQL, после того как установите указываете имя пользователя, пароль и название БД в файле настроек `test_case\settings.py (DATABASES)`
Создаем и применяем необходимые миграции командой
```
python manage.py makemigrations api
python manage.py migrate
```

После того, как миграции будут применены и таблицы в БД создадутся, нам нужно наполнить их данными. Для этого мы можем использовать скрипт `script.py`, просто запустив его командой:
```
python script.py
```

Данный скрипт создает пять должностей:
+ Teamlead
+ Senior
+ Middle
+ Junior
+ Trainee

В данной иерархии подразумевается, что `Teamlead` стоит во главе иерархии и у него есть подопечные `Senior`, у которых также есть подопечные с должностью `Middle` и т.д.
Также скрипт генерирует 50000 работников и наполняет ими базу данных.


## Структура базы данных
Есть две основные таблицы БД: `api_employee` & `api_job_title`. `Api_job_title` состоит из двух столбцов `id` и `title`, где `title` название должности, чем меньше число `id`, тем выше работник стоит в иерархии, то есть должность с `id = 0` является наивысшей должностью. `Api_job_title` включает в себя основные данные о работнике, указанные в ТЗ, а также дополнительные столбцы: `salary_currency, username, password, auth_token`, где `chef_id` - id начальника данного работника.


## API Endpoints
После того как мы запустим скрипт командой:
```
python manage.py runserver
```
нам будут доступны следующие эндпоинты

```JSON
POST /api/login/

Request:
{
  "username": "username",
  "password": "123456"
}

Response:
{
  "msg": "success",
  "token": "bf1238a0e7e319536292bb58434117cc0e1ed2ba08ce807cdecb44edf3734a43" //Используется для валидации пользователя
}
```

```JSON
POST /api/logout/

Request:
{
  "token": "bf1238a0e7e319536292bb58434117cc0e1ed2ba08ce807cdecb44edf3734a43"
}

Response:
{
  "msg": "successfully logout!"
}
```

```JSON
GET /api/job_titles/

Request:
{
  "token": "bf1238a0e7e319536292bb58434117cc0e1ed2ba08ce807cdecb44edf3734a43"
}

Response:
[
    {
        "id": 0,
        "title": "Teamlead"
    },
    {
        "id": 1,
        "title": "Senior"
    },
    {
        "id": 2,
        "title": "Middle"
    },
    {
        "id": 3,
        "title": "Junior"
    },
    {
        "id": 4,
        "title": "Trainee"
    }
]
```
```JSON
GET /api/abilities/ 

Request:
{
  "token": "bf1238a0e7e319536292bb58434117cc0e1ed2ba08ce807cdecb44edf3734a43"
}

Response:
{
    "msg": "Functionality available to you", //Получаем функции которые нам доступны
    "params": {
        "search_by": [
            "id",
            "first_name",
            "second_name",
            "middle_name",
            "job_title",
            "hired",
            "salary",
            "chief",
            "username"
        ],
        "ordering_by": [
            "id",
            "first_name",
            "second_name",
            "middle_name",
            "job_title",
            "hired",
            "salary",
            "chief",
            "username"
        ],
        "reversed_ordering": [
            "False",
            "True"
        ],
        "tree": [
            "False",
            "True"
        ]
    }
}
```
```JSON
GET /api/getempolyers/

Request:
{
  "token": "bf1238a0e7e319536292bb58434117cc0e1ed2ba08ce807cdecb44edf3734a43",
  "reversed_ordering": "True", //Сортировка элементов в обратном порядке
  "ordering_by": "first_name", //Определяет по какому полю сортируем данные
  "tree": "True", //Выводить данные в виде древа вместе с подчиненными, если False, то выводит только самих работников без подчиненных
  "search_by": { //Ищем только по определенному критерию
    "param": "id", где id = 0
    "value": "0"
  }
}

Response:
{
    "count": 1,
    "next": null, //Присутствует пагинация, что бы сильно не грузить сервер/ПК
    "previous": null,
    "results": [
        {
            "id": 0,
            "first_name": "Герман",
            "second_name": "Чистяков",
            "middle_name": "Прохорович",
            "hired": "2022-08-03",
            "salary": "567.00 USD",
            "chief_name": null,
            "username": "username0",
            "job_title": "Teamlead",
            "children": [
                {
                    "id": 1,
                    "first_name": "Рюрик",
                    "second_name": "Бабышев",
                    "middle_name": "Карлович",
                    "hired": "2022-08-03",
                    "salary": "991.00 USD",
                    "chief_name": "Герман Чистяков Прохорович",
                    "username": "username1",
                    "job_title": "Senior",
                    "children": [
                        {
                            "id": 3,
                            "first_name": "Василий",
                            "second_name": "Шапиро",
                            "middle_name": "Сократович",
                            "hired": "2022-08-03",
                            "salary": "1269.00 USD",
                            "chief_name": "Рюрик Бабышев Карлович",
                            "username": "username3",
                            "job_title": "Middle",
                            "children": [
                                {
                                    "id": 4,
                                    "first_name": "Юрий",
                                    "second_name": "Шапиро",
                                    "middle_name": "Сократович",
                                    "hired": "2022-08-03",
                                    "salary": "1114.00 USD",
                                    "chief_name": "Василий Шапиро Сократович",
                                    "username": "username4",
                                    "job_title": "Junior",
                                    "children": [
                                        {
                                            "id": 5,
                                            "first_name": "Владислав",
                                            "second_name": "Шапиро",
                                            "middle_name": "Никифорович",
                                            "hired": "2022-08-03",
                                            "salary": "1029.00 USD",
                                            "chief_name": "Юрий Шапиро Сократович",
                                            "username": "username5",
                                            "job_title": "Trainee",
                                            "children": []
                                        },
                                        {
                                            "id": 6,
                                            "first_name": "Юрий",
                                            "second_name": "Ивашев",
                                            "middle_name": "Иосифович",
                                            "hired": "2022-08-03",
                                            "salary": "1547.00 USD",
                                            "chief_name": "Юрий Шапиро Сократович",
                                            "username": "username6",
                                            "job_title": "Trainee",
                                            "children": []
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "id": 2,
                            "first_name": "Юрий",
                            "second_name": "Корниенко",
                            "middle_name": "Прохорович",
                            "hired": "2022-08-03",
                            "salary": "1567.00 USD",
                            "chief_name": "Рюрик Бабышев Карлович",
                            "username": "username2",
                            "job_title": "Middle",
                            "children": []
                        }
                    ]
                }
            ]
        }
    ]
}
```
```JSON
POST /api/changedata/

Request:
{
    "token": "fc96b55306cc7a5fadf067bc73b496acdc91adda5a60a7f64723b3650b781fbb",
    "first_name": "Владилен" //Позволяет изменить абсолютно любое поле в базе данных, просто нужно указать название таблицы и новое значение
}

Response:
{
    "msg": "success"
}
```

```JSON
POST /api/changepassword/

Request:
{
    "token": "2c77f787c419a88f0bf1a0337434e0a0801975d03a436056c10f621452a346b5",
    "old_password": "123456",
    "new_password": "123456789"
}

Response:
{
    "msg": "password succesfully changed!"
}
```
