from . import db
from werkzeug.security import generate_password_hash, check_password_hash

class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(128))

    def __repr__(self):
        return f'id:{self.id}, username:{self.username}'


    def set_password(self, password):
        self.password = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password, password)


    def is_active(self):
        # Возвращаем True, если пользователь активен
        return True
    

    def get_id(self):
        return str(self.id)
    

    def is_authenticated(self):
    # Возвращает True, если пользователь аутентифицирован
        return True


class book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cover_photo = db.Column(db.Text)
    title = db.Column(db.String(400))
    author = db.Column(db.String(400))
    num_pages = db.Column(db.Integer)
    publisher = db.Column(db.String(400))
