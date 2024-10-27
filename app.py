from flask import Flask, url_for, redirect, render_template
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

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

@app.route("/lab1/cause_error")
def cause_error():
    return 1 / 0

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

@app.route("/lab1")
def lab1():
    return '''
<!doctype html>
<html>
    <head>
        <title>Лабораторная 1</title>
    </head>
    <body>
        <h1>Лабораторная 1</h1>
        <p>
            Flask — фреймворк для создания веб-приложений на языке программирования Python, 
            использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2. 
            Относится к категории так называемых микрофреймворков — минималистичных каркасов 
            веб-приложений, сознательно предоставляющих лишь самые базовые возможности.
        </p>
        <h2>Список роутов</h2>
            <ul>
                <li><a href="/lab1/cause_error">Вызов ошибки 500</a></li>
                <li><a href="/lab1/web">web</a></li>
                <li><a href="/lab1/author">Автор</a></li>
                <li><a href="/lab1/oak">Дуб</a></li>
                <li><a href="/lab1/counter">Счётчик</a></li>
                <li><a href="/lab1/info">Инфо</a></li>
                <li><a href="/lab1/created">Создано</a></li>
                <li><a href="/lab1/about_winter">Зима</a></li>
            </ul>
        <a href="''' + url_for('index') + '''">На главную</a>
    </body>
</html>
'''

@app.route("/lab1/web")
def web():
    return """<!doctype html>
        <html>
           <body>
               <h1>web-сервер на flask</h1>
               <a href="/lab1/author">author</a>
           </body>
        </html>""", 200, {
            'X-Server': 'sample',
            'Content-Type': 'text/plain; charset=utf-8'
            }

@app.route("/lab1/author")
def author():
    name = "Втюрина Наталья Артёмовна"
    group = "ФБИ-24"
    faculty = "ФБ"

    return """<!doctype html>
        <html>
           <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Факультет: """ + faculty + """</p>
                <a href="/lab1/web">web</a>
            </body>
        </html>"""

@app.route("/lab1/oak")
def oak():
    path = url_for("static", filename="oak.jpg")
    css_path = url_for("static", filename="lab1.css")
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="''' + css_path + '''">
    </head>
    <body>
        <h1>Дуб</h1>
        <img src="''' + path + '''">
    </body>
</html>
'''

count = 0
@app.route("/lab1/counter")
def counter():
    global count
    count +=1
    return '''
<!doctype html>
<html>
    <body>
        <h1>Сколько раз вы заходили сюда: ''' + str(count) + '''</h1>
        <a href="''' + url_for('reset_counter') + '''">Очистить счётчик</a>
    </body>
</html>
'''

@app.route("/lab1/reset_counter")
def reset_counter():
    global count
    count = 0  
    return redirect(url_for('counter'))

@app.route("/lab1/info")
def info():
    return redirect("/author")

@app.route("/lab1/created")
def created():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то создано...</i></div>
    </body>
</html>
''', 201

@app.route("/lab1/about_winter")
def about_winter():
    winterpic = url_for("static", filename="winter.jpeg")
    return '''
<!doctype html>
<html lang="ru">
<head>
    <title>Зима</title>
</head>
<body>
        <h1>Конец зимы</h1>
        <p>
            Конец зимы. Солнце светит в полную силу, а снежок под его лучами превращается 
            в пушистую белую вату. В это время особенно хочется тепла, солнца и хорошего настроения. 
            В воздухе чувствуется запах весны. И на улице становится всё теплее. Зима понемногу отступает 
            и дарит нам теплую весну. Уже сейчас можно увидеть первые цветы. Лепестки подснежников напоминают 
            нам о том, что скоро наступит весна... Скоро... Скоро весна и нас ожидает много новых открытий и 
            впечатлений. Но, а пока, мы можем любоваться ее прилётом. Я люблю смотреть на весну и ждать ее 
            прихода.
        </p>
        <p>
            Конец зимы, начало весны. Время, когда природа просыпается от зимнего сна и начинает дарить 
            нам свои краски. В это время года мы можем наблюдать за пробуждением природы. Природа просыпается 
            и постепенно оживает. Первые весенние цветы, распускаются на деревьях, кустарниках, которые 
            покрываются первыми листиками. На полянах появляются первые цветы. Постепенно все вокруг зеленеет. 
            Как будто природа надевает свои лучшие наряды. И наступает праздник для всей природы.
        </p>
        <p>
            Конец зимы природа встречает теплыми деньками. Снег еще не успел растаять, а с крыш капают 
            первые весенние капли. Как только на деревьях появляются первые листочки, все вокруг преображается. 
            В воздухе витает аромат весны. Настроение у всех приподнятое. Вот и сегодня, в этот солнечный денек, 
            мы всей семьей отправились на прогулку.
        </p>
        <img src="''' + winterpic + '''">
    </div>
</body>
</html> ''',{
    'Content-Language': 'ru',
    'X-Student-Project': 'Winter',
    'X-Author-Name': 'Dzen-Class'
}

@app.route('/lab2/a')
def a():
    return 'ok'

@app.route('/lab2/a/')
def a2():
    return 'со слэшем'

flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']

@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        return "такого цветка нет", 404
    else:
        return f'''
<!doctype html>
<html>
    <body>
        <h1>Цветок: {flower_list[flower_id]}</h1>
        <p><a href="/lab2/flowers">Посмотреть все цветы</a></p>
    </body>
</html>
'''

@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    if not name:
        abort(400, description="вы не задали имя цветка")
    flower_list.append(name)
    return f'''
<!doctype html>
<html>
    <body>
        <h1>Добавлен новый цветок</h1>
        <p>Название нового цветка: {name} </p>
        <p>Всего цветов: {len(flower_list)} </p>
        <p>Полный список: {flower_list} </p>
        <p><a href="/lab2/flowers">Посмотреть все цветы</a></p>
    </body>
</html>
'''

@app.route('/lab2/flowers')
def all_flowers():
    flowers_html = ''.join(f'<li>{flower}</li>' for flower in flower_list)
    return f'''
<!doctype html>
<html>
    <body>
        <h1>Все цветы</h1>
        <p>Количество цветов: {len(flower_list)}</p>
        <ul>{flowers_html}</ul>
        <p><a href="/lab2/clear_flowers">Очистить список цветов</a></p>
    </body>
</html>
'''

@app.route('/lab2/clear_flowers')
def clear_flowers():
    flower_list.clear()
    return '''
<!doctype html>
<html>
    <body>
        <h1>Список цветов очищен</h1>
        <p>Все цветы удалены.</p>
        <p><a href="/lab2/flowers">Посмотреть все цветы</a></p>
    </body>
</html>
'''

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