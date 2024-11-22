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


