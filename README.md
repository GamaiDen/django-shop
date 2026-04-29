# Django Shop

Интернет-магазин на Django.

## Функциональность
- Каталог товаров с CRUD
- Блог
- Регистрация и авторизация (AbstractUser, email)
- Права доступа: владелец + модератор
- Валидация форм (запрещённые слова, цена)
- Кастомная группа "Модератор продуктов"

## Установка
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
