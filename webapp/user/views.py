from webapp.user.forms import LoginForm, RegistrationForm
from webapp.user.models import User
from webapp import db
from flask_login import login_user, logout_user, current_user
from flask import render_template, flash, redirect, url_for, Blueprint
from webapp.utils import get_redirect_target

blueprint = Blueprint('user', __name__, url_prefix='/users')


@blueprint.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(get_redirect_target())
    page_title = 'Авторизация'
    login_form = LoginForm()
    return render_template('user/login.html', page_title=page_title, form=login_form)


@blueprint.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password_hash(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Вы успешно вошли на сайт')
            return redirect(get_redirect_target())
    flash('Неправильные имя или пароль')
    return redirect(get_redirect_target())


@blueprint.route('/logout')
def logout():
    logout_user()
    flash('Вы успешно разлогинились')
    return redirect(get_redirect_target())


@blueprint.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('news.index'))
    page_title = 'Регистрация'
    form = RegistrationForm()
    return render_template('user/registration.html', page_title=page_title, form=form)


@blueprint.route('/process-reg', methods=['POST'])
def process_reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, role='user')
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Вы успешно зарегестрировались!')
        return redirect(url_for('user.login'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Ошибка в поле "{getattr(form, field).label.text}": {error}')
        return redirect(url_for('user.register'))
