from flask import Flask, url_for, redirect, render_template, request
from werkzeug.exceptions import HTTPException
from lab1 import lab1

app = Flask(__name__)
app.register_blueprint(lab1)

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
                    <li><a href="''' + url_for('lab1') + '''">Первая лабораторная</a></li>
                    <li><a href="''' + url_for('lab2') + '''">Вторая лабораторная</a></li>
                </ul>
            </div>
        </main>
        <footer>
            <p>Втюрина Наталья Артёмовна, группа ФБИ-24, 3 курс, 2024 год</p>
        </footer>
    </body>
</html>
'''

@app.route('/lab2/a')
def a():
    return 'ok'

@app.route('/lab2/a/')
def a2():
    return 'со слэшем'

flowers_list = [
    {"name": "Роза", "price": 250},
    {"name": "Тюльпан", "price": 150},
    {"name": "Незабудка", "price": 160},
    {"name": "Ромашка", "price": 120}
]

@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flowers_list):
        return "такого цветка нет", 404
    else:
        flower = flowers_list[flower_id]
        return render_template('flower.html', flower=flower, flower_id=flower_id)

@app.route('/lab2/add_flower', methods=['POST'])
def add_flower():
    name = request.form.get('name')
    price = request.form.get('price')
    if not name or not price:
        abort(400, description="вы не задали имя или цену цветка")
    flowers_list.append({"name": name, "price": int(price)})
    return redirect(url_for('all_flowers'))

@app.route('/lab2/flowers/')
def all_flowers():
    return render_template('flowers.html', flowers=flowers_list)

@app.route('/lab2/clear_flowers')
def clear_flowers():
    flowers_list.clear()
    return redirect(url_for('all_flowers'))

@app.route('/lab2/delete_flower/<int:flower_id>')
def delete_flower(flower_id):
    if flower_id >= len(flowers_list):
        return "такого цветка нет", 404
    else:
        del flowers_list[flower_id]
        return redirect(url_for('all_flowers'))

@app.route('/lab2/example')
def example():
    name, lab_num, year_num, group = 'Втюрина Наталья', '2', '3 курс', 'ФБИ-24'
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321}
    ]
    return render_template('example.html',
                            name = name, lab_num = lab_num, year_num = year_num,
                            group = group, fruits = fruits)

@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase = phrase)

@app.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    return render_template('calc.html', a = a, b = b)

@app.route('/lab2/calc/')
def default_calc():
    return redirect('/lab2/calc/1/1')

@app.route('/lab2/calc/<int:a>')
def single_param_calc(a):
    return redirect(f'/lab2/calc/{a}/1')

books = [
        {"author": "Джордж Оруэлл", "title": "1984", "genre": "Дистопия", "pages": 328},
        {"author": "Харпер Ли", "title": "Убить пересмешника", "genre": "Классика", "pages": 281},
        {"author": "Дж.К. Роулинг", "title": "Гарри Поттер и философский камень", "genre": "Фэнтези", "pages": 223},
        {"author": "Дж.Р.Р. Толкин", "title": "Хоббит", "genre": "Фэнтези", "pages": 310},
        {"author": "Ф. Скотт Фицджеральд", "title": "Великий Гэтсби", "genre": "Классика", "pages": 180},
        {"author": "Герман Мелвилл", "title": "Моби Дик", "genre": "Приключения", "pages": 635},
        {"author": "Джейн Остин", "title": "Гордость и предубеждение", "genre": "Романтика", "pages": 279},
        {"author": "Марк Шусак", "title": "Книжный вор", "genre": "Историческая проза", "pages": 552},
        {"author": "Габриэль Гарсиа Маркес", "title": "Сто лет одиночества", "genre": "Магический реализм", "pages": 417},
        {"author": "Халед Хоссейни", "title": "Бегущий за ветром", "genre": "Историческая проза", "pages": 372}
    ]

@app.route('/lab2/books')
def show_books():
    return render_template('book.html', books=books)

berries = [
    {"name": "Клубника", "description": "Сладкая и сочная, популярная летняя ягода.", "image": "strawberry.jpg"},
    {"name": "Малина", "description": "Мелкая, кисло-сладкая ягода любима за свой аромат.", "image": "raspberry.jpg"},
    {"name": "Черника", "description": "Темно-синяя ягода богата антоцианами.", "image": "blueberry.jpeg"},
    {"name": "Крыжовник", "description": "Кисловатая ягода, часто используется в джемах.", "image": "gooseberry.jpg"},
    {"name": "Ежевика", "description": "Сладкая и ароматная ягода чёрного цвета.", "image": "blackberry.webp"}
]

@app.route('/lab2/berries')
def show_berries():
    return render_template('berries.html', berries=berries)