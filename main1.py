from flask import Flask, render_template, redirect
from data import session
from data import users
from data import jobs
from data.jobs import Jobs
import datetime
from flask_login import LoginManager, login_user
from forms.user import RegisterForm, LoginForm, AddJobsForm
from API import news_api, jobs_api

app = Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)
app.config['SECRET_KEY'] = 'grgrgr'

login_manager = LoginManager()
login_manager.init_app(app)
session.global_init("db/users.db")


@login_manager.user_loader
def load_user(user_id):
    db_sess = session.create_session()
    return db_sess.query(users.User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = session.create_session()
        user = db_sess.query(users.User).filter(users.User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = session.create_session()
        if db_sess.query(users.User).filter(users.User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = users.User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/')
def main():
    db_sess = session.create_session()
    jobs = db_sess.query(Jobs)
    return render_template('jobs.html', title='Работа', jobs=jobs)


@app.route('/addjob', methods=['GET', 'POST'])
def addjob():
    # search for water below the surface
    form = AddJobsForm()
    if form.validate_on_submit():
        db_sess = session.create_session()

        job = jobs.Jobs(
            job=form.job.data,
            team_leader=form.team_leader.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data
        )

        db_sess.add(job)
        db_sess.commit()
        return redirect("/")

    return render_template('job.html', title='Adding a job', form=form)


app.register_blueprint(jobs_api.jobs_blueprint)

if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1')
