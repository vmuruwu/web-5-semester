from flask import Flask, url_for, redirect
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

