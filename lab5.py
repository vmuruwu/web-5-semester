from flask import Blueprint, render_template, request, redirect, session, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

lab5 = Blueprint('lab5', __name__)


@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html', login=session.get('login'))


def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host = '127.0.0.1',
            database = 'natalya_vtyurina_knowledge_base',
            user = 'natalya_vtyurina_knowledge_base',
            password = '123'  
        )
        cur = conn.cursor(cursor_factory = RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    
    return conn, cur

def db_close(conn, cur):
    try:
        # Для PostgreSQL
        if current_app.config['DB_TYPE'] == 'postgres' and conn and not conn.closed:
            conn.commit()
        # Для SQLite
        elif current_app.config['DB_TYPE'] != 'postgres' and conn:
            conn.commit()
    except Exception as e:
        print(f"Ошибка при commit: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            try:
                conn.close()
            except Exception as e:
                print(f"Ошибка при закрытии соединения: {e}")


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
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM users WHERE login=%s;", (login, ))
        else:
            cur.execute("SELECT * FROM users WHERE login=?;", (login, ))
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
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM users WHERE login=%s;", (login, ))
        else:
            cur.execute("SELECT * FROM users WHERE login=?;", (login, ))
        if cur.fetchone():
            return render_template('lab5/register.html', error="Такой пользователь уже существует")
        
        password_hash = generate_password_hash(password)
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("INSERT INTO users (login, password) VALUES (%s, %s);", (login, password_hash))
        else:
            cur.execute("INSERT INTO users (login, password) VALUES (?, ?);", (login, password_hash))
        return render_template('lab5/success.html', login=login)
    
    finally:
        db_close(conn, cur)


@lab5.route('/lab5/list')
def list_articles():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()

    try:
        if login:
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("SELECT id FROM users WHERE login=%s;", (login, ))
            else:
                cur.execute("SELECT id FROM users WHERE login=?;", (login, ))
            user_id = cur.fetchone()['id']

            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("""
                    SELECT * FROM articles 
                    WHERE user_id=%s OR is_public=TRUE 
                    ORDER BY is_favorite DESC;
                """, (user_id,))
            else:
                cur.execute("""
                    SELECT * FROM articles 
                    WHERE user_id=? OR is_public=1 
                    ORDER BY is_favorite DESC;
                """, (user_id,))
                
        else:
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("SELECT * FROM articles WHERE is_public=TRUE;") 
            else:
                cur.execute("SELECT * FROM articles WHERE is_public=1;")    
        articles = cur.fetchall()

        db_close(conn, cur)
        return render_template('/lab5/articles.html', articles=articles)

    finally:
        db_close(conn, cur)



@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    if request.method == 'GET':
        return render_template('lab5/create_article.html')

    title = request.form.get('title', '').strip()
    article_text = request.form.get('article_text', '').strip()

    if not title or not article_text:
        return render_template('lab5/create_article.html', 
                               error="Название и текст статьи не могут быть пустыми")

    conn, cur = db_connect()
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM users WHERE login=%s", (login,))
        else:
            cur.execute("SELECT * FROM users WHERE login=?", (login,))
        user_id = cur.fetchone()["id"]

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("INSERT INTO articles(user_id, tittle, article_text) VALUES (%s, %s, %s);", 
                        (user_id, title, article_text))
        else:
            cur.execute("INSERT INTO articles(user_id, tittle, article_text) VALUES (?, ?, ?);", 
                        (user_id, title, article_text))
    finally:
        db_close(conn, cur)

    return redirect('/lab5/list')


@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None) 
    return redirect('/lab5') 


@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM users WHERE login=%s", (login,))
        else:
            cur.execute("SELECT * FROM users WHERE login=?", (login,))
        user_id = cur.fetchone()["id"]

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM articles WHERE id=%s AND user_id=%s", (article_id, user_id))
        else:
            cur.execute("SELECT * FROM articles WHERE id=? AND user_id=?", (article_id, user_id))
        article = cur.fetchone()

        if not article:
            return redirect('/lab5/list')

        if request.method == 'GET':
            return render_template('lab5/edit_article.html', article=article)

        title = request.form.get('title')
        article_text = request.form.get('article_text')

        if not title or not article_text:
            return render_template('lab5/edit_article.html', article=article, error="Все поля обязательны для заполнения.")

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute(
                "UPDATE articles SET tittle=%s, article_text=%s WHERE id=%s AND user_id=%s",
                (title, article_text, article_id, user_id)
            )
        else:
            cur.execute(
                "UPDATE articles SET tittle=?, article_text=? WHERE id=? AND user_id=?",
                (title, article_text, article_id, user_id)
            )

        conn.commit()
        return redirect('/lab5/list')

    finally:
        db_close(conn, cur)


@lab5.route('/lab5/delete/<int:article_id>', methods=['POST'])
def delete_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM users WHERE login=%s", (login,))
        else:
            cur.execute("SELECT * FROM users WHERE login=?", (login,))
        user_id = cur.fetchone()["id"]

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM articles WHERE id=%s AND user_id=%s", (article_id, user_id))
        else:
            cur.execute("SELECT * FROM articles WHERE id=? AND user_id=?", (article_id, user_id))
        article = cur.fetchone()

        if not article:
            return redirect('/lab5/list')

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("DELETE FROM articles WHERE id=%s AND user_id=%s", (article_id, user_id))
        else:
            cur.execute("DELETE FROM articles WHERE id=? AND user_id=?", (article_id, user_id))

        conn.commit()
        return redirect('/lab5/list')

    finally:
        db_close(conn, cur)


@lab5.route('/lab5/users')
def users_list():
    login = session.get('login')
    conn, cur = db_connect()

    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT login FROM users;")
        else:
            cur.execute("SELECT login FROM users;")
        users = cur.fetchall()

        return render_template('lab5/users.html', users=users)
    finally:
        db_close(conn, cur)


@lab5.route('/lab5/favorite/<int:article_id>', methods=['POST'])
def toggle_favorite(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT is_favorite FROM articles WHERE id=%s;", (article_id,))
        else:
            cur.execute("SELECT is_favorite FROM articles WHERE id=?;", (article_id,))
        
        article = cur.fetchone()
        if not article:
            return "Статья не найдена", 404

        new_status = not article['is_favorite']

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE articles SET is_favorite=%s WHERE id=%s;", (new_status, article_id))
        else:
            cur.execute("UPDATE articles SET is_favorite=? WHERE id=?;", (new_status, article_id))
        
        conn.commit()
        return redirect('/lab5/list')
    finally:
        db_close(conn, cur)

@lab5.route('/lab5/public/<int:article_id>', methods=['POST'])
def toggle_public(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT is_public FROM articles WHERE id=%s;", (article_id,))
        else:
            cur.execute("SELECT is_public FROM articles WHERE id=?;", (article_id,))
        
        article = cur.fetchone()
        if not article:
            return "Статья не найдена", 404

        new_status = not article['is_public']
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE articles SET is_public=%s WHERE id=%s;", (new_status, article_id))
        else:
            cur.execute("UPDATE articles SET is_public=? WHERE id=?;", (new_status, article_id))
        
        conn.commit()
        return redirect('/lab5/list')
    finally:
        db_close(conn, cur)


@lab5.route('/lab5/like/<int:article_id>', methods=['POST'])
def like_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE articles SET likes = likes + 1 WHERE id=%s;", (article_id,))
        else:
            cur.execute("UPDATE articles SET likes = likes + 1 WHERE id=?;", (article_id,))
        
        conn.commit()
        return redirect('/lab5/list')
    finally:
        db_close(conn, cur)