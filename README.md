# alpha_soft_task_tracker
---
### 1. Виртуальное окружение
**Windows**
```
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux**
```
python3 -m venv venv
source venv/bin/activate
```
---
### 2. Зависимости
```
pip install -r requirements.txt
```
---
### 3. Миграции и суперпользователь
```
python manage.py migrate
python manage.py createsuperuser
```
---
### 4. Запуск сервера
```
python manage.py runserver
```
---
### 5. Регистрация нового пользователя (Postman)
POST запрос

http://127.0.0.1:8000/auth/users/

Body
raw JSON
```
{
  "username": "username",
  "password": "password",
  "email": "email"
}
```
(email необязательно)
---
### 6. Получение JWT-токена
POST запрос

http://127.0.0.1:8000/auth/jwt/create/

Body
raw JSON
```
{
  "username": "username",
  "password": "password"
}
```
берем из ответа токен с ключом "access"
---
### 7. Обращение к эндпоинтам /api/...
GET запрос 

http://127.0.0.1:8000/api/...

Authorization

Auth Type: Bearer Token
```
Token: access_token
```
---
### Документация
http://127.0.0.1:8000/redoc/

http://127.0.0.1:8000/swagger/
