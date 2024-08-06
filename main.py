
from flask import Flask, redirect, url_for, render_template, flash, request
from flask_login import login_user, LoginManager, logout_user, login_required, UserMixin, current_user
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap5
from sqlalchemy import Integer, String, Text, ForeignKey, Date
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, TextAreaField, DateField, RadioField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = "TODOLIST"
Bootstrap5(app)

login_manager = LoginManager()
login_manager.init_app(app)


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ToDo.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


class ToDo(db.Model):
    __tablename__ = "to_do"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    task_title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    priority: Mapped[str] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(50), default='todo')
    user = relationship('User', back_populates='tasks')


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(1000))
    tasks = relationship('ToDo', back_populates='user')


class ToDoForm(FlaskForm):
    task_title = StringField('Task Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    date = DateField('Due Date', format='%Y-%m-%d', validators=[DataRequired()])
    priority = RadioField('Priority', choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
                          validators=[DataRequired()])


class RegisterForm(FlaskForm):
    name = StringField("Name",validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign up")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
    submit = SubmitField("Log in")


with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        email = request.form.get('email')
        user_db = db.session.execute(db.select(User). where(User.email == email))
        user = user_db.scalar()
        if user:
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        new_user = User(
            email=request.form.get('email'),
            password=generate_password_hash(password=request.form.get('password'),method="pbkdf2",salt_length=8),
            name=request.form.get('name')
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("get_all_task"))
    return render_template("register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        # Find user by email entered.
        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()

        if user and check_password_hash(user.password, password):
            login_user(user)
            print(user)
            flash('You were successfully logged in.')
            return redirect(url_for('get_all_task'))
        elif not user:
            flash("Your email doesn't exists.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash("Your Password is incorrect.")
            return redirect(url_for('login'))
        # elif not user:
        #     flash("Your email doesn't exists.")
        #     return redirect(url_for('login'))
    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/')
def home():
    return redirect(url_for("register"))


@app.route('/home')
@login_required
def get_all_task():
    tasks = ToDo.query.filter_by(user_id=current_user.id).all()
    form = ToDoForm()
    return render_template("index.html", form=form, tasks=tasks)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def home_page():
    form = ToDoForm()
    if form.validate_on_submit():
        new_task = ToDo(
            user_id=current_user.id,
            task_title=form.task_title.data,
            description=form.description.data,
            date=form.date.data,
            priority=form.priority.data
        )

        db.session.add(new_task)
        db.session.commit()
        print(current_user.id)
        return redirect(url_for('get_all_task'))
    tasks = ToDo.query.filter_by(user_id=current_user.id).all()

    return render_template("index.html", form=form, all_tasks=tasks)


@app.route('/move_task/<int:task_id>/<string:new_status>')
@login_required
def move_task(task_id, new_status):
    task = ToDo.query.get(task_id)
    if task:
        task.status = new_status
        db.session.commit()
        flash(f'Task "{task.task_title}" moved to {new_status.capitalize()}!', 'success')
    else:
        flash('Task not found!', 'danger')
    return redirect(url_for('get_all_task'))


@app.route('/delete/<int:task_id>')
@login_required
def delete_task(task_id):
    task_to_delete = db.get_or_404(ToDo, task_id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_task'))


if __name__ == '__main__':
    app.run(debug=True)
