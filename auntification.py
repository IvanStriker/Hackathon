
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from modals import db, User
import re
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


def validate_registration(form_data):
    """Валидация данных регистрации"""
    errors = {}

    # Проверка имени пользователя
    username = form_data.get('username', '').strip()
    if not username:
        errors['username'] = 'Имя пользователя обязательно'
    elif len(username) < 1:
        errors['username'] = 'Имя пользователя должно быть не менее 2 символов'
    elif not re.match(r'^[a-zA-Z0-9_]+$', username):
        errors['username'] = 'Можно использовать только буквы, цифры и подчеркивание'

    # Проверка email
    email = form_data.get('email', '').strip()
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not email:
        errors['email'] = 'Email обязателен'
    elif not re.match(email_regex, email):
        errors['email'] = 'Введите корректный email'

    # Проверка пароля
    password = form_data.get('password', '')
    confirm_password = form_data.get('confirm_password', '')

    if not password:
        errors['password'] = 'Пароль обязателен'
    elif len(password) < 6:
        errors['password'] = 'Пароль должен быть не менее 6 символов'
    elif password != confirm_password:
        errors['confirm_password'] = 'Пароли не совпадают'

    return errors


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Получаем данные из формы
        form_data = {
            'username': request.form.get('username'),
            'email': request.form.get('email'),
            'password': request.form.get('password'),
            'confirm_password': request.form.get('confirm_password'),
            'first_name': request.form.get('first_name'),
            'last_name': request.form.get('last_name'),
            'bio': request.form.get('bio')
        }

        # Валидация
        errors = validate_registration(form_data)

        # Проверяем уникальность в БД
        if not errors.get('username'):
            existing_user = User.query.filter_by(username=form_data['username']).first()
            if existing_user:
                errors['username'] = 'Это имя пользователя уже занято'

        if not errors.get('email'):
            existing_email = User.query.filter_by(email=form_data['email']).first()
            if existing_email:
                errors['email'] = 'Этот email уже используется'

        # Если есть ошибки - показываем форму снова
        if errors:
            return render_template('auth/register.html',
                                   errors=errors,
                                   form_data=form_data)

        try:
            # Создаем пользователя
            user = User(
                username=form_data['username'],
                email=form_data['email'],
                first_name=form_data['first_name'] if form_data['first_name'] else None,
                last_name=form_data['last_name'] if form_data['last_name'] else None,
                bio=form_data['bio'] if form_data['bio'] else None
            )

            # Устанавливаем пароль
            user.set_password(form_data['password'])

            # Сохраняем в БД
            db.session.add(user)
            db.session.commit()

            # Отправляем email приветствия (опционально)
            # send_welcome_email(user.email, user.username)

            # Уведомляем об успехе
            flash('🎉 Регистрация успешна! Теперь вы можете войти в систему.', 'success')

            # Перенаправляем на страницу входа
            return redirect(url_for('auth.login'))

        except Exception as e:
            # Откатываем изменения в случае ошибки
            db.session.rollback()
            current_app.logger.error(f'Ошибка при регистрации: {e}')

            # Показываем ошибку пользователю
            flash('Произошла ошибка при регистрации. Попробуйте позже.', 'error')

            return render_template('auth/register.html',
                                   errors={'general': 'Ошибка сервера'},
                                   form_data=form_data)

    # GET запрос - показываем форму
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = bool(request.form.get('remember'))

        # Ищем пользователя по username или email
        user = User.query.filter(
            (User.username == username) | (User.email == username)
        ).first()

        if user and user.check_password(password):
            if user.is_active:
                # Обновляем время последнего входа
                user.last_login = datetime.utcnow()
                db.session.commit()

                # Авторизуем пользователя
                login_user(user, remember=remember)

                flash(f'👋 Добро пожаловать, {user.get_full_name()}!', 'success')

                # Перенаправляем на главную или следующую страницу
                next_page = request.args.get('next')
                if not next_page or not next_page.startswith('/'):
                    next_page = url_for('main.index')
                return redirect(next_page)
            else:
                flash('Ваш аккаунт деактивирован', 'error')
        else:
            flash('Неверное имя пользователя или пароль', 'error')

    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('main.index'))


@auth_bp.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html', user=current_user)