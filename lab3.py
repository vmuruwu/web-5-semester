from flask import Blueprint, url_for, redirect, render_template, request, make_response, abort
lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name', 'аноним')
    name_color = request.cookies.get('name_color', 'неизвестный')
    age = request.cookies.get('age', 'не указан')
    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)


@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Natalya', max_age=5)
    resp.set_cookie('age', '21')
    resp.set_cookie('name_color', 'magenta')
    return resp


@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp


@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'

    age = request.args.get('age')
    if age == '':
        errors['age'] = 'Заполните поле!'
    
    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)


@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')


@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    # Пусть кофе стоит 120 рублей, чёрный чай — 80 рублей, зелёный — 70 рублей.
    if drink == 'coffee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    # Добавка молока удорожает напиток на 30 рублей, а сахара — на 10.
    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template('lab3/pay.html', price=price)


@lab3.route('/lab3/success')
def success():
    price = request.args.get('price')
    return render_template('lab3/success.html', price=price)


@lab3.route('/lab3/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        color = request.form.get('color')
        bgcolor = request.form.get('bgcolor')
        fontsize = request.form.get('fontsize')
        fontfamily = request.form.get('fontfamily')

        response = make_response(render_template('lab3/settings.html', color=color, bgcolor=bgcolor, fontsize=fontsize, fontfamily=fontfamily))
        response.set_cookie('color', color)
        response.set_cookie('bgcolor', bgcolor)
        response.set_cookie('fontsize', fontsize)
        response.set_cookie('fontfamily', fontfamily)
        return response

    color = request.cookies.get('color')
    bgcolor = request.cookies.get('bgcolor')
    fontsize = request.cookies.get('fontsize')
    fontfamily = request.cookies.get('fontfamily')

    return render_template('lab3/settings.html', color=color, bgcolor=bgcolor, fontsize=fontsize, fontfamily=fontfamily)


@lab3.route('/lab3/clear_settings')
def clear_settings():
    response = make_response(redirect(url_for('lab3.settings')))
    response.delete_cookie('color')
    response.delete_cookie('bgcolor')
    response.delete_cookie('fontsize')
    response.delete_cookie('fontfamily')
    return response


@lab3.route('/lab3/ticket_form')
def ticket_form():
    return render_template('lab3/ticket_form.html')

@lab3.route('/lab3/process_ticket', methods=['POST'])
def process_ticket():
    fio = request.form.get('fio')
    berth = request.form.get('berth')
    linen = 'on' if request.form.get('linen') else 'off'
    luggage = 'on' if request.form.get('luggage') else 'off'
    age = request.form.get('age')
    departure = request.form.get('departure')
    destination = request.form.get('destination')
    date = request.form.get('date')
    insurance = 'on' if request.form.get('insurance') else 'off'
    
    # Проверка обязательных полей
    if not all([fio, berth, age, departure, destination, date]) or not (1 <= int(age) <= 120):
        abort(400, description="Одно или несколько полей не заполнены или неверный возраст.")
    
    # Рассчет стоимости
    if int(age) < 18:
        ticket_type = "Детский билет"
        price = 700
    else:
        ticket_type = "Взрослый билет"
        price = 1000
    
    if berth == "нижняя" or berth == "нижняя боковая":
        price += 100
    
    if linen == "on":
        price += 75
    
    if luggage == "on":
        price += 250
    
    if insurance == "on":
        price += 150
    
    return render_template('lab3/ticket.html', fio=fio, berth=berth, linen=linen, luggage=luggage, 
                           age=age, departure=departure, destination=destination, date=date, 
                           insurance=insurance, ticket_type=ticket_type, price=price)


products = [
    {"name": "Смартфон A", "price": 15000, "brand": "Samsung", "color": "Черный"},
    {"name": "Смартфон B", "price": 25000, "brand": "LG", "color": "Белый"},
    {"name": "Ноутбук A", "price": 55000, "brand": "Samsung", "color": "Серый"},
    {"name": "Ноутбук B", "price": 75000, "brand": "LG", "color": "Синий"},
    {"name": "Планшет A", "price": 20000, "brand": "Samsung", "color": "Красный"},
    {"name": "Планшет B", "price": 30000, "brand": "LG", "color": "Зеленый"},
    {"name": "Телевизор A", "price": 45000, "brand": "Samsung", "color": "Черный"},
    {"name": "Телевизор B", "price": 65000, "brand": "LG", "color": "Белый"},
    {"name": "Часы A", "price": 5000, "brand": "Samsung", "color": "Серебристый"},
    {"name": "Часы B", "price": 10000, "brand": "LG", "color": "Золотистый"},
    {"name": "Камера A", "price": 30000, "brand": "Samsung", "color": "Черный"},
    {"name": "Камера B", "price": 45000, "brand": "LG", "color": "Белый"},
    {"name": "Наушники A", "price": 3000, "brand": "Samsung", "color": "Синий"},
    {"name": "Наушники B", "price": 7000, "brand": "LG", "color": "Зеленый"},
    {"name": "Колонка A", "price": 8000, "brand": "Samsung", "color": "Красный"},
    {"name": "Колонка B", "price": 12000, "brand": "LG", "color": "Черный"},
    {"name": "Монитор A", "price": 20000, "brand": "Samsung", "color": "Серый"},
    {"name": "Монитор B", "price": 35000, "brand": "LG", "color": "Белый"},
    {"name": "Клавиатура A", "price": 2500, "brand": "Samsung", "color": "Черный"},
    {"name": "Клавиатура B", "price": 4500, "brand": "LG", "color": "Белый"}
]


@lab3.route('/lab3/product_search', methods=['GET', 'POST'])
def product_search():
    min_price = request.args.get('min_price', type=int)
    max_price = request.args.get('max_price', type=int)
    
    if min_price is None or max_price is None:
        return render_template('lab3/product_search.html')
    
    filtered_products = [product for product in products if min_price <= product["price"] <= max_price]
    
    return render_template('lab3/product_results.html', products=filtered_products, min_price=min_price, max_price=max_price)