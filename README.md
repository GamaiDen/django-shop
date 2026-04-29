# Django Shop

Интернет-магазин на Django.

## Функциональность
- Каталог товаров с CRUD
- Блог с публикациями
- Регистрация и авторизация пользователей
- Валидация форм (запрещённые слова, цена)
- Отправка email при регистрации
- Защита CRUD через login_required

## Установка
```bash
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver

