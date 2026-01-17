# Веб-приложение «Каталог книг»

## Описание
В этом сайте пользователи могут управлять списком книг.

## Используемые бибиотеки и фрэмворки

#### Фронтэнд:
- Jinja2
- Bootstrap 5
#### Бэкэнд:
- Flask
- SQL ALchemy
- Flask Migration

## Архитектура:
- MVC

## Структура:
# Структура проекта:

```
book-catalog-app/
├── api/
│   ├── __init__.py
│   ├── deps.py
|   └── endpoints         
├── core/                       
│   ├── __init__.py
│   └── config.py           
├── db/                           
│   ├── __init__.py
│   ├── base.py                 
│   └── session.py               
├── migrations/                  
│   ├── versions/                
│   │   └── 42355a96f17f_initial_migration.py
│   ├── README                   
│   ├── alembic.ini              
│   ├── env.py                   
│   └── script.py.mako
├── models/                       
│   ├── __init__.py
│   ├── book.py                  
│   ├── user.py                  
│   └── userbook.py              
├── schemas/                     
│   ├── __init__.py
│   ├── book.py                
│   └── user.py                  
├── static/
│       ├── img
|       |   └── Error-404-Page
│       └── books
│           └── literature.json  
├── utilits/ 
│   └── read_json.py
├── templates/                   
│   ├── authorization/            
│   │   ├── login.html
│   │   └── register.html
│   ├── book/                    
│   │   └── list.html
│   ├── user/                    
│   │   ├── archive.html          
│   │   ├── delete.html
│   │   ├── detail.html
│   │   ├── list.html
│   │   ├── update.html
│   │   └── user.html
│   ├── 404_error.html            
│   ├── base.html                 
│   └── home.html              
├── app.py                        
```

## Ход реализации

#### 1. Устновка и активация виртуальной среды:
- `python -m venv .venv` создание виртуальной среды.

- `/.env/scripts/activate` активация виртуальной среды.

- `pip install flask sqlalchemy flask-migration` устновка нужных библиотек к виртуальной среды.

- `pip freeze > requirements.txt` создание файла requirements для деплоя.

#### 2. Создание обектов:
- Пользователь\
&emsp;&emsp;&emsp;+ id\
&emsp;&emsp;&emsp;+ имя\
&emsp;&emsp;&emsp;+ почта\
&emsp;&emsp;&emsp;+ каталог
- Книга\
&emsp;&emsp;&emsp;+ id\
&emsp;&emsp;&emsp;+ название\
&emsp;&emsp;&emsp;+ автор\
&emsp;&emsp;&emsp;+ год издания\
&emsp;&emsp;&emsp;+ жанр\
&emsp;&emsp;&emsp;+ краткое описание\
&emsp;&emsp;&emsp;+ статус чтения (не начата / читаю / прочитана)





## Features
#### Пользователь может:

- добавлять книги в каталог
- редактировать сведения
- удалять записи
- отмечать статус чтения
- просматривать каталог


## API Reference

#### Get home page

```http
  GET /
```
#выдает основную страницу сайта

#### Get user

```http
GET /user/<string:name>
```

| Parameter | Type     | Description                           |
| :-------- | :------- | :------------------------------------ |
| `name`      | `string` | **Required**. Name of user to fetch |

#### Get user list

```http
GET /users
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `None`    | `None`   | Load user list                    |

#### Post users

```http
POST /users ??
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |


#### Get user

```http
GET /user/<int:id>/create ??
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |


#### Get user information detail

```http
GET /user/<int:id>/detail
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of user to fetch |

#### Get page to update user information

```http
GET /user/<int:id>/update
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of user to update. Load the page to update.|


#### Update user information

```http
POST /user/<int:id>/update
```

| Parameter | Type     | Description                        |
| :-------- | :------- | :--------------------------------- |
| `id`      | `string` | **Required**. Id of user to update.|


#### Get user
```http
GET /user/<int:id>/delete
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |


#### Get user

```http
GET /user/<int:id>/archive
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |

#### Get user

```http
GET /user/<int:user_id>/archive/book/<int:book_id>/add
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |


#### Get user

```http
GET /user/<int:user_id>/archive/book/<int:book_id>/remove
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |

#### Get user
```http
GET /user/<int:user_id>/archive/book/<int:book_id>/status/update
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |

#### Get user
```http
GET /books
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |

#### Get user
```http
GET /login", methods=["POST", "GET"]
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |

#### Get user
```http
GET /logout", methods=["POST", "GET"]
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |

#### Get user
```http
GET /register", methods=["GET", "POST"]
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |

#### Get user
```http
GET /.well-known/appspecific/com.chrome.devtools.json
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |


#### Get user

```http
GET /users/create", methods=["GET", "POST"]
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |

#### add(num1, num2)

Takes two numbers and returns the sum.

## Запуск

Проект запускается с помощью команды 
```http
flask run
```
которая содержит app.py

## Участники 

1. Панфилова Анна 
2. Виноградов Иван 
3. Симина Елизавета
4. Дао Мань Зыонг

## Скринкаст

[см. google drive](https://drive.google.com/file/d/1VubG2k2f6lctuzlF88hefTEUGU1snbuY/view?usp=sharing)