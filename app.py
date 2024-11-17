from flask import Flask, url_for, redirect, render_template, request
from werkzeug.exceptions import HTTPException
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4

app = Flask(__name__)
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)


@app.errorhandler(404)
def not_found(err):
    path404 = url_for("static", filename="404.css")
    img404 = url_for("static", filename="2034479.png")
    return '''
<!doctype html>
<html>
    <head>
        <title>Страница не найдена (404)</title>
        <link rel="stylesheet" href="'''+ path404 + '''">
    </head>
<body>
    <div class="container">
        <h1>Упс! Страница не найдена</h1>
        <p>Страница, которую вы ищете, не существует.</p>
        <img src="''' + img404 + '''" alt="Страница не найдена">
        <p><a href="''' + url_for('index') + '''">Вернуться на главную страницу</a></p>
    </div>
</body>
</html>''', 404


@app.errorhandler(500)
def internal_server_error(err):
    path404 = url_for("static", filename="404.css")
    return '''
<!doctype html>
<html>
    <head>
        <title>Ошибка 500 — Внутренняя ошибка сервера</title>
        <link rel="stylesheet" href="'''+ path404 + '''">
    </head>
    <body>
        <div class="container">
            <h1>Ой! Что-то пошло не так.</h1>
            <p>На сервере произошла внутренняя ошибка. Попробуйте позже.</p>
            <p><a href="''' + url_for('index') + '''">Вернуться на главную страницу</a></p>
        </div>
    </body>
</html>
''', 500


@app.errorhandler(400)
def bad_request(err):
    return "Неправильный запрос", 400


@app.errorhandler(401)
def unauthorized(err):
    return "Требуется авторизация", 401

@app.errorhandler(403)
def forbidden(err):
    return "Доступ запрещен", 403


@app.errorhandler(405)
def method_not_allowed(err):
    return "Метод не разрешен", 405


@app.errorhandler(418)
def im_a_teapot(err):
    return "Я чайник", 418


@app.route("/")
@app.route("/index")
def index():
    return '''
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <header>
            <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
        </header>
        <main>
            <div>
                <ul>
                    <li><a href="''' + url_for('lab1.lab') + '''">Первая лабораторная</a></li>
                    <li><a href="''' + url_for('lab2.lab') + '''">Вторая лабораторная</a></li>
                    <li><a href="''' + url_for('lab3.lab') + '''">Третья лабораторная</a></li>
                    <li><a href="''' + url_for('lab4.lab') + '''">Четвёртая лабораторная</a></li>
                </ul>
            </div>
        </main>
        <footer>
            <p>Втюрина Наталья Артёмовна, группа ФБИ-24, 3 курс, 2024 год</p>
        </footer>
    </body>
</html>
'''
