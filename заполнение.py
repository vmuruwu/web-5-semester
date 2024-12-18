import requests
from db import db
from db.models import book
from flask import Flask

# Создаем экземпляр Flask-приложения
app = Flask(__name__)

# Настройки для базы данных
user_db = "user"
password = "123"
host_ip = "127.0.0.1"
host_port = "5432"
database_name = "bd_user"

# Строка подключения для SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user_db}:{password}@{host_ip}:{host_port}/{database_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Функция для получения данных о книгах из Google Books API
def fetch_books_from_api(start_index=0, max_results=10):
    books = []
    url = "https://www.googleapis.com/books/v1/volumes"
    
    # Параметры запроса
    params = {
        'q': 'book',  # Ключевое слово для поиска
        'maxResults': max_results,  # Количество книг на запрос
        'startIndex': start_index  # Начальный индекс для пагинации
    }
    
    response = requests.get(url, params=params)
    
    # Проверка успешности запроса
    if response.status_code != 200:
        print(f"Ошибка запроса: {response.status_code}")
        return books

    data = response.json()

    # Выводим полученные данные для отладки
    print(data)

    # Проверяем, есть ли в ответе ключ 'items'
    if 'items' not in data:
        print("В ответе нет ключа 'items'. Возможно, ошибка в запросе.")
        return books

    # Проходим по результатам и извлекаем нужные данные
    for item in data['items']:
        title = item['volumeInfo'].get('title', 'No title')
        author = ', '.join(item['volumeInfo'].get('authors', ['Unknown author']))
        publisher = item['volumeInfo'].get('publisher', 'Unknown publisher')
        num_pages = item['volumeInfo'].get('pageCount', 0)
        cover_photo = item['volumeInfo'].get('imageLinks', {}).get('thumbnail', None)

        # Создаем объект книги
        new_book = book(
            title=title,
            cover_photo=cover_photo,
            author=author,
            num_pages=num_pages,
            publisher=publisher
        )
        books.append(new_book)

    return books

# Вставка книг в базу данных
def insert_books_to_db():
    all_books = []
    total_books_to_fetch = 50  # Общее количество книг для получения
    max_results = 10  # Количество книг, которые мы хотим получать за один запрос
    num_requests = total_books_to_fetch // max_results  # Количество запросов

    for i in range(num_requests):
        start_index = i * max_results
        books = fetch_books_from_api(start_index=start_index, max_results=max_results)
        all_books.extend(books)
    
    if all_books:
        with app.app_context():  # Убедитесь, что находитесь в контексте приложения
            db.session.bulk_save_objects(all_books)  # Быстрая вставка нескольких объектов
            db.session.commit()
            print(f"Вставлено {len(all_books)} книг в базу данных.")
    else:
        print("Не удалось получить книги.")

# Вставка книг в базу
insert_books_to_db()
