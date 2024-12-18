from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, login_required, current_user, logout_user, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
import re
from flask_migrate import Migrate

app = Flask(__name__)

# Конфигурация для базы данных SQLite
app.secret_key = "123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Используем SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализация базы данных и миграций
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Инициализация Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.init_app(app)

# Модели базы данных (например, для пользователей и книг)
class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    cover_photo = db.Column(db.String(200), nullable=True)
    author = db.Column(db.String(100), nullable=False)
    num_pages = db.Column(db.Integer, nullable=False)
    publisher = db.Column(db.String(100), nullable=False)

# Загрузка пользователя для Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))

# Главная страница
@app.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    offset = (page - 1) * per_page
    
    total_books = book.query.count()
    books = book.query.offset(offset).limit(per_page).all()
    return render_template('rgz/index.html', books=books, page=page, per_page=per_page, total_books=total_books)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form.get('query')
        mode = request.form.get('mode')
        sort = request.form.get('sort')
        min_pages = request.form.get('min_pages')
        max_pages = request.form.get('max_pages')
    else:
        query = request.args.get('query')
        mode = request.args.get('mode')
        sort = request.args.get('sort')
        min_pages = request.args.get('min_pages')
        max_pages = request.args.get('max_pages')

    if query:
        books = filter_books(query, mode)
    else:
        books = book.query

    if min_pages and max_pages:
        if min_pages is None or max_pages is None:
            print("Кто-то ищет без значений")
        else:
            books = filter_books_by_pages(books, int(min_pages), int(max_pages))

    if sort:
        books = sort_books(books, sort)

    page = request.args.get('page', 1, type=int)
    per_page = 20
    offset = (page - 1) * per_page
    
    total_books = books.count()
    books = books.offset(offset).limit(per_page).all()
    return render_template('rgz/search.html', books=books, page=page, per_page=per_page, total_books=total_books, query=query, mode=mode, sort=sort, min_pages=min_pages, max_pages=max_pages)

def filter_books(query, mode):
    if mode == 'title':
        return book.query.filter(book.title.ilike(f"%{query}%"))
    elif mode == 'author':
        return book.query.filter(book.author.ilike(f"%{query}%"))
    elif mode == 'publisher':
        return book.query.filter(book.publisher.ilike(f"%{query}%"))
    else:
        return book.query

def sort_books(books, sort):
    if sort == 'title':
        return books.order_by(book.title.asc())
    elif sort == 'author':
        return books.order_by(book.author.asc())
    elif sort == 'pages':
        return books.order_by(book.num_pages.asc())
    elif sort == 'publisher':
        return books.order_by(book.publisher.asc())
    else:
        return books

def filter_books_by_pages(books, min_pages, max_pages):
    return books.filter(book.num_pages.between(min_pages, max_pages))

# Страница регистрации
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("rgz/register.html")

    username_form = request.form.get("username")
    password_form = request.form.get("password")

    isUserExist = users.query.filter_by(username=username_form).first()

    errors = []

    if isUserExist is not None:
        errors.append("Такой пользователь уже существует!")
        return render_template("rgz/register.html", errors=errors)
    elif not username_form:
        errors.append("Введите имя пользователя!")
        return render_template("rgz/register.html", errors=errors)
    elif not re.match("^[a-zA-Z0-9]+$", password_form):  # Проверка на наличие только букв и цифр
        errors.append("Пароль должен содержать только буквы и цифры!")
        return render_template("rgz/register.html", errors=errors)
    elif re.search("[а-яА-Я]", password_form):  # Проверка на наличие русских символов
        errors.append("Пароль не должен содержать русские буквы!")
        return render_template("rgz/register.html", errors=errors)
    elif len(password_form) < 5:
        errors.append("Пароль должен содержать не менее 5 символов!")
        return render_template("rgz/register.html", errors=errors)

    hashedPswd = generate_password_hash(password_form, method="pbkdf2")

    newUser = users(username=username_form, password=hashedPswd)

    db.session.add(newUser)

    db.session.commit()

    return redirect("/login")

# Страница авторизации
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("rgz/login.html")

    if current_user.is_authenticated:  # Если пользователь уже авторизован, перенаправляем его на другую страницу
        return redirect(url_for('search'))

    if request.method == "POST":
        errors = []
        username_form = request.form.get("username")
        password_form = request.form.get("password")

        my_user = users.query.filter_by(username=username_form).first()

        if my_user is not None:
            if check_password_hash(my_user.password, password_form):
                login_user(my_user, remember=False)
                return redirect(url_for('search'))

        if not (username_form or password_form):
            errors.append("Введите имя пользователя и пароль!")
        elif my_user is None or not check_password_hash(my_user.password, password_form):
            errors.append("Неверное имя пользователя или пароль!")

        return render_template("rgz/login.html", errors=errors)

    return render_template("rgz/login.html")

# Страница выхода из системы
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы успешно вышли из системы.', 'success')
    return redirect(url_for('index'))

# Страница создания книги
@app.route('/create_book', methods=['GET', 'POST'])
@login_required
def create_book():
    if request.method == 'POST':
        title = request.form['title']
        cover_photo = request.form['cover_photo']
        author = request.form['author']
        num_pages = request.form['num_pages']
        publisher = request.form['publisher']
            
        new_book = book(title=title, cover_photo=cover_photo, author=author, num_pages=num_pages, publisher=publisher)
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('rgz/create_book.html')

# Страница редактирования книги
@app.route('/edit_book', methods=['GET', 'POST'])
@login_required
def edit_book():
    list_books_for = book.query.all()
    book_to_edit = None
    
    if request.method == 'POST':
        book_for_id = request.form['id']
        book_to_edit = book.query.get(book_for_id)
        book_to_edit.title = request.form['title']
        book_to_edit.cover_photo = request.form['cover_photo']
        book_to_edit.author = request.form['author']
        
        num_pages = request.form['num_pages']
        if num_pages.isdigit():
            book_to_edit.num_pages = int(num_pages)
        
        publisher = request.form['publisher']
        if publisher.isdigit():
            book_to_edit.publisher = int(publisher)
        
        db.session.commit()

        return redirect(url_for('search'))

    return render_template('rgz/edit_book.html', book=book_to_edit, list_books_for=list_books_for)

# Страница удаления книги
@app.route('/delete_book', methods=['GET', 'POST'])
@login_required
def delete_book():
    list_books_for = book.query.all()
    book_to_delete = None

    if request.method == 'POST':
        book_id = request.form['id']
        book_to_delete = book.query.get(book_id)
        list_books_for = book.query.all()

        if book_to_delete:
            db.session.delete(book_to_delete)
            db.session.commit()

            return redirect(url_for('index'))

    return render_template('rgz/delete_book.html', books=list_books_for, book=book_to_delete)

if __name__ == "__main__":
    app.run(debug=True)
