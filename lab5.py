from flask import Blueprint, render_template, request, redirect, session
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash

lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html', login=session.get('login'))

def db_connect():
    conn = psycopg2.connect(
        host = '127.0.0.1',
        database = 'natalya_vtyurina_knowledge_base',
        user = 'natalya_vtyurina_knowledge_base',
        password = '123'  
    )
    cur = conn.cursor(cursor_factory = RealDictCursor)

    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not (login and password):  
        return render_template('lab5/login.html', error="Заполните поля")
    
    conn, cur = db_connect()  

    try:
        cur.execute(f"SELECT * FROM users WHERE login=%s;", (login,))
        user = cur.fetchone()

        if not user:
            db_close(conn, cur)  
            return render_template('lab5/login.html', error='Логин и/или пароль неверны')

        if not check_password_hash(user['password'], password):
            db_close(conn, cur)  
            return render_template('lab5/login.html', error='Пароль введён неверно')
        
        session['login'] = login
        return render_template('lab5/success_login.html', login=login)

    finally:
        db_close(conn, cur)  
        

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login and password):  
        return render_template('lab5/register.html', error='Заполните все поля')

    conn, cur = db_connect()  

    try:
        cur.execute(f"SELECT login FROM users WHERE login=%s;", (login,))
        if cur.fetchone():
            return render_template('lab5/register.html', error="Такой пользователь уже существует")
        
        password_hash = generate_password_hash(password)
        cur.execute(f"INSERT INTO users (login, password) VALUES (%s, %s);", (login, password_hash))
        return render_template('lab5/success.html', login=login)
    
    finally:
        db_close(conn, cur)  



@lab5.route('/lab5/list')
def list_articles():
    return "Список статей"


@lab5.route('/lab5/create')
def create_article():
    return "Создать статью"
