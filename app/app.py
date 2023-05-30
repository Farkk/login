from flask import Flask, render_template, flash, redirect, url_for
from flask_login import login_user, LoginManager
from markupsafe import Markup
from flask_sqlalchemy import SQLAlchemy
from app.components.forms import LoginForm, RegistrForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your-secret-key'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
id = 0


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    def get_id(self):
        return str(self.id)

    def is_active(self):
        return True


@app.route('/', methods=["POST", "GET"])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        remember = True if form.remember.data else False

        if user is None or not user.password:
            flash(Markup('Email or password is incorrect, please try again'))
            return redirect('/')

        login_user(user, remember=remember)
        return redirect(url_for('main'))

    return render_template("index.html", form=form)


@app.route('/signup', methods=["POST", "GET"])
def signUp():
    global id
    form = RegistrForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()  # Проверка есть ли с таким email

        if user:
            flash(Markup('User with this email already exists. Go to <a href="login">login page</a>.'))
            return redirect(url_for('signup'))  # Переадресация на эту же страницу, чтобы flash отобразилс

        new_user = Users(email=form.email.data,
                         password=form.password.data,
                         id=id)

        db.session.add(new_user)
        db.session.commit()
        id += 1
        return redirect("/")
    return render_template("registr.html", form=form)


@app.route('/main')
def main():
    return render_template("main.html")


def run():
    with app.app_context():
        db.create_all()
    app.run(debug=True)
