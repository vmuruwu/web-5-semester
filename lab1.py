from flask import Blueprint, url_for, redirect
lab1 = Blueprint('lab1', __name__)


@lab1.route("/lab1/cause_error")
def cause_error():
    return 1 / 0


@lab1.route("/lab1")
def lab():
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


@lab1.route("/lab1/web")
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


@lab1.route("/lab1/author")
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


@lab1.route("/lab1/oak")
def oak():
    path = url_for("static", filename="lab1/oak.jpg")
    css_path = url_for("static", filename="lab1/lab1.css")
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
@lab1.route("/lab1/counter")
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


@lab1.route("/lab1/reset_counter")
def reset_counter():
    global count
    count = 0  
    return redirect(url_for('counter'))


@lab1.route("/lab1/info")
def info():
    return redirect("/author")


@lab1.route("/lab1/created")
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


@lab1.route("/lab1/about_winter")
def about_winter():
    winterpic = url_for("static", filename="lab1/winter.jpeg")
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