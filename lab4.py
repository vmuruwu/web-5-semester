from flask import Blueprint, render_template, request, redirect, session
lab4 = Blueprint('lab4', __name__)

@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')


@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')


@lab4.route('/lab4/div', methods = ['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error = 'Оба поля должны быть заполнены!')
    if x2 == '0':
        return render_template('lab4/div.html', error = 'Деление на 0!')
    x1 = int(x1)
    x2 = int(x2)
    result = x1/x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('lab4/sum-form.html')


@lab4.route('/lab4/sum', methods = ['POST'])
def sum():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '':
        x1=0
    if x2 == '':
        x2=0
    x1 = int(x1)
    x2 = int(x2)
    result = x1+x2
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/diff-form')
def diff_form():
    return render_template('lab4/diff-form.html')


@lab4.route('/lab4/diff', methods = ['POST'])
def diff():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/diff.html', error = 'Оба поля должны быть заполнены!')
    x1 = int(x1)
    x2 = int(x2)
    result = x1-x2
    return render_template('lab4/diff.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/expo-form')
def expo_form():
    return render_template('lab4/expo-form.html')


@lab4.route('/lab4/expo', methods = ['POST'])
def expo():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/expo.html', error = 'Оба поля должны быть заполнены!')
    if x1 == '0' and x2 == '0':
        return render_template('lab4/expo.html', error = 'Оба поля не должны быть равны нулю!')
    x1 = int(x1)
    x2 = int(x2)
    result = x1**x2
    return render_template('lab4/expo.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/mult-form')
def mult_form():
    return render_template('lab4/mult-form.html')


@lab4.route('/lab4/mult', methods = ['POST'])
def mult():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '':
        x1=1
    if x2 == '':
        x2=1
    x1 = int(x1)
    x2 = int(x2)
    result = x1*x2
    return render_template('lab4/mult.html', x1=x1, x2=x2, result=result)


tree_count = 0

@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count)
    operation = request.form.get('operation')
    if operation == 'cut' and tree_count > 0:
        tree_count -= 1
    elif operation == 'plant' and tree_count < 10:
        tree_count += 1
    return redirect('/lab4/tree')


users = [
    {'login': 'alex', 'password': '123', 'name': 'Александр Смит', 'gender': 'мужской'},
    {'login': 'bob', 'password': '555', 'name': 'Боб Джонсон', 'gender': 'мужской'},
    {'login': 'sara', 'password': '789', 'name': 'Сара Коннор', 'gender': 'женский'},
    {'login': 'marisha', 'password': '222', 'name': 'Мариша Миллер', 'gender': 'женский'}
]

@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            user_login = session['login']
            user = next((user for user in users if user['login'] == user_login), None)
            name = user['name'] if user else ''
        else:
            authorized = False
            user_login = ''
            name = ''
        return render_template('lab4/login.html', authorized=authorized, login=user_login, name=name)

    login = request.form.get('login')
    password = request.form.get('password')

    if not login:
        error = 'Не введён логин'
    elif not password:
        error = 'Не введён пароль'
    else:
        for user in users:
            if login == user['login'] and password == user['password']:
                session['login'] = login
                return redirect('/lab4/login')
        error = 'Неверные логин и/или пароль'

    return render_template('lab4/login.html', error=error, login=login, authorized=False)


@lab4.route('/lab4/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')


@lab4.route('/lab4/registration', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        name = request.form.get('name')
        gender = request.form.get('gender')

        if not login or not password or not name or not gender:
            error = 'Все поля должны быть заполнены'
            return render_template('lab4/registration.html', error=error)

        if any(user['login'] == login for user in users):
            error = 'Логин уже занят'
            return render_template('lab4/registration.html', error=error)

        users.append({'login': login, 'password': password, 'name': name, 'gender': gender})
        return redirect('/lab4/login')

    return render_template('lab4/registration.html')


@lab4.route('/lab4/users')
def list_users():
    if 'login' not in session:
        return redirect('/lab4/login')
    
    return render_template('lab4/users.html', users=users)


@lab4.route('/lab4/edit-user', methods=['GET', 'POST'])
def edit_user():
    if 'login' not in session:
        return redirect('/lab4/login')

    user_login = session['login']
    user = next((user for user in users if user['login'] == user_login), None)

    if request.method == 'POST':
        new_name = request.form.get('name')
        new_password = request.form.get('password')
        if new_name:
            user['name'] = new_name
        if new_password:
            user['password'] = new_password
        return redirect('/lab4/users')

    return render_template('lab4/edit-user.html', user=user)


@lab4.route('/lab4/delete-user', methods=['POST'])
def delete_user():
    if 'login' not in session:
        return redirect('/lab4/login')

    user_login = session.pop('login', None)
    global users
    users = [user for user in users if user['login'] != user_login]
    return redirect('/lab4/login')


@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    if request.method == 'POST':
        temperature = request.form.get('temperature')

        if not temperature:
            error = 'Ошибка: не задана температура'
            return render_template('/lab4/fridge.html', error=error)
        
        try:
            temperature = int(temperature)
        except ValueError:
            error = 'Ошибка: неверный формат температуры'
            return render_template('/lab4/fridge.html', error=error)

        if temperature < -12:
            error = 'Не удалось установить температуру — слишком низкое значение'
            return render_template('/lab4/fridge.html', error=error)
        elif temperature > -1:
            error = 'Не удалось установить температуру — слишком высокое значение'
            return render_template('/lab4/fridge.html', error=error)
        elif -12 <= temperature <= -9:
            message = f'Установлена температура: {temperature}°С'
            snowflakes = '❄❄❄'
        elif -8 <= temperature <= -5:
            message = f'Установлена температура: {temperature}°С'
            snowflakes = '❄❄'
        elif -4 <= temperature <= -1:
            message = f'Установлена температура: {temperature}°С'
            snowflakes = '❄'

        return render_template('/lab4/fridge.html', message=message, snowflakes=snowflakes)
    return render_template('/lab4/fridge.html')


grain_prices = {
    'ячмень': 12345,
    'овёс': 8522,
    'пшеница': 8722,
    'рожь': 14111
}

@lab4.route('/lab4/order-grain', methods=['GET', 'POST'])
def order_grain():
    if request.method == 'POST':
        grain_type = request.form.get('grain_type')
        weight = request.form.get('weight')
        
        if not weight:
            error = 'Ошибка: не указан вес'
            return render_template('lab4/order_grain.html', error=error)
        try:
            weight = float(weight)
        except ValueError:
            error = 'Ошибка: вес должен быть числом'
            return render_template('lab4/order_grain.html', error=error)

        if weight <= 0:
            error = 'Ошибка: вес должен быть больше 0'
            return render_template('lab4/order_grain.html', error=error)

        if grain_type not in grain_prices:
            error = 'Ошибка: выбранное зерно недоступно'
            return render_template('lab4/order_grain.html', error=error)

        if weight > 500:
            error = 'Ошибка: такого объема сейчас нет в наличии'
            return render_template('lab4/order_grain.html', error=error)

        price_per_ton = grain_prices[grain_type]
        total_price = weight * price_per_ton
        discount = 0

        if weight > 50:
            discount = 0.10
            total_price *= (1 - discount)

        message = (f'Заказ успешно сформирован. Вы заказали {grain_type}.'
                   f'Вес: {weight} т. Сумма к оплате: {total_price:.2f} руб.')
        if discount > 0:
            message += f' Применена скидка за большой объем: 10%.'

        return render_template('lab4/order_grain.html', message=message)
    
    return render_template('lab4/order_grain.html')

