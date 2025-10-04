# 🕸️ Web Scraper & Admin Panel - Портфолио Проект
**Функционал:**
* Асинхронный **Парсинг** данных (товары, вакансии, новости).
* **Сохранение** данных в **Excel** и **Базу Данных (SQL)**.
* Мини-**Админ-панель** для **Выгрузки/Фильтрации** данных.
* Использование **Background Tasks** для неблокирующего запуска парсинга.
  
**Стек технологий:**
* Python 3.11+
* **FastAPI** / **Jinja2**
* **SQLAlchemy 2.0+**
* **BeautifulSoup / httpx**
* **Pandas / openpyxl**
* SQLite
---
## ⚙️ Установка (ctrl c, ctrl v)
### 1. Клонирование репозитория
```bash
git clone https://github.com/ev3ryy/URL-Parser.git
cd Web-Scraper-Admin-Panel
```
### 2. Установка зависимостей
```
pip install -r requirements.txt
```
### 3. Запуск
```
python app/main.py
```
