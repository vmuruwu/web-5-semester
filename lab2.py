from flask import Blueprint, url_for, redirect
lab2 = Blueprint('lab2', __name__)


@lab2.route('/lab2/a')
def a():
    return 'ok'


@lab2.route('/lab2/a/')
def a2():
    return 'со слэшем'


flowers_list = [
    {"name": "Роза", "price": 250},
    {"name": "Тюльпан", "price": 150},
    {"name": "Незабудка", "price": 160},
    {"name": "Ромашка", "price": 120}
]


@lab2.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flowers_list):
        return "такого цветка нет", 404
    else:
        flower = flowers_list[flower_id]
        return render_template('flower.html', flower=flower, flower_id=flower_id)


@lab2.route('/lab2/add_flower', methods=['POST'])
def add_flower():
    name = request.form.get('name')
    price = request.form.get('price')
    if not name or not price:
        abort(400, description="вы не задали имя или цену цветка")
    flowers_list.append({"name": name, "price": int(price)})
    return redirect(url_for('all_flowers'))


@lab2.route('/lab2/flowers/')
def all_flowers():
    return render_template('flowers.html', flowers=flowers_list)


@lab2.route('/lab2/clear_flowers')
def clear_flowers():
    flowers_list.clear()
    return redirect(url_for('all_flowers'))


@lab2.route('/lab2/delete_flower/<int:flower_id>')
def delete_flower(flower_id):
    if flower_id >= len(flowers_list):
        return "такого цветка нет", 404
    else:
        del flowers_list[flower_id]
        return redirect(url_for('all_flowers'))


@lab2.route('/lab2/example')
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


@lab2.route('/lab2/')
def lab2():
    return render_template('lab2.html')


@lab2.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase = phrase)


@lab2.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    return render_template('calc.html', a = a, b = b)


@lab2.route('/lab2/calc/')
def default_calc():
    return redirect('/lab2/calc/1/1')


@lab2.route('/lab2/calc/<int:a>')
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


@lab2.route('/lab2/books')
def show_books():
    return render_template('book.html', books=books)


berries = [
    {"name": "Клубника", "description": "Сладкая и сочная, популярная летняя ягода.", "image": "strawberry.jpg"},
    {"name": "Малина", "description": "Мелкая, кисло-сладкая ягода любима за свой аромат.", "image": "raspberry.jpg"},
    {"name": "Черника", "description": "Темно-синяя ягода богата антоцианами.", "image": "blueberry.jpeg"},
    {"name": "Крыжовник", "description": "Кисловатая ягода, часто используется в джемах.", "image": "gooseberry.jpg"},
    {"name": "Ежевика", "description": "Сладкая и ароматная ягода чёрного цвета.", "image": "blackberry.webp"}
]


@lab2.route('/lab2/berries')
def show_berries():
    return render_template('berries.html', berries=berries)