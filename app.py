# app.py
from flask import Flask, render_template
from flask_login import LoginManager
from modals import db, User


app = Flask(__name__)

# Конфигурация
app.config['SECRET_KEY'] = 'ваш-секретный-ключ-изменяйте-это'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///booksite.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Инициализация расширений
db.init_app(app)

# Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Пожалуйста, войдите для доступа к этой странице.'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Регистрация блюпринтов
app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)


# Главная страница
@app.route('/')
def index():
    return render_template('index.html')


# Обработчик ошибок
@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500


# Инициализация БД
def init_database():
    with app.app_context():
        db.create_all()

        # Создаем администратора если его нет
        if User.query.filter_by(username='root').count() == 0:
            admin = User(
                username='root',
                email='root@booksite.ru',
                first_name='Администратор',
                is_admin=True
            )
            admin.set_password('toor')
            db.session.add(admin)
            db.session.commit()
            print('✅ Администратор создан')


if __name__ == '__main__':
    init_database()
    app.run(debug=True)