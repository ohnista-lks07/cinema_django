# Cinema Django Project
Це Django-проєкт для роботи з фільмами.
Дозволяє зберігати, фільтрувати та сортувати фільми за допомогою ORM-запитів.

---

## Технології

* Python 3.13
* Django 6.0.3

---

## Як запустити проєкт

1. Клонувати репозиторій:
   git clone https://github.com/ohnista-lks07/cinema_django.git

2. Перейти в папку проєкту:
   cd cinema_django

3. Створити віртуальне середовище:
   python -m venv .venv

4. Активувати середовище:
   Mac:
   source .venv/bin/activate

5. Встановити Django:
   pip install django

6. Застосувати міграції:
   python manage.py migrate

7. Запустити сервер:
   python manage.py runserver

---

## Моделі

### Genre

* **name** — назва жанру

### Director

* **first_name** — ім’я
* **last_name** — прізвище
* **birth_year** — рік народження
* **country** — країна

### Movie

* **title** — назва фільму
* **year** — рік випуску
* **rating** — рейтинг
* **duration** — тривалість (хвилини)
* **is_public** — чи доступний публічно
* **created_at** — дата створення
* **genre** — жанр (ForeignKey → Genre)
* **director** — режисер (за ключем)

### Review

* **movie** — фільм (за ключем)
* **text** — текст відгуку
* **score** — оцінка
* **created_at** — дата створення

---

## Запити

Усі 15 ORM-запитів реалізовані у файлі `queries.py`.

---
