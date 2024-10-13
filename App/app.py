pip install Flask Flask-SQLAlchemy Flask-Login Flask-WTF
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from forms import RegistrationForm, LoginForm, TicketForm, OrderForm
from models import User, Ticket, Order
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 用户注册
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# 用户登录
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('tickets'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

# 显示票务
@app.route("/tickets")
@login_required
def tickets():
    tickets = Ticket.query.all()
    return render_template('tickets.html', tickets=tickets)

# 添加票务
@app.route("/add_ticket", methods=['GET', 'POST'])
@login_required
def add_ticket():
    form = TicketForm()
    if form.validate_on_submit():
        ticket = Ticket(event_name=form.event_name.data, event_date=form.event_date.data, price=form.price.data, available_tickets=form.available_tickets.data)
        db.session.add(ticket)
        db.session.commit()
        flash('Ticket added successfully!', 'success')
        return redirect(url_for('tickets'))
    return render_template('add_ticket.html', form=form)

# 订单处理
@app.route("/order/<int:ticket_id>", methods=['GET', 'POST'])
@login_required
def order(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    form = OrderForm()
    if form.validate_on_submit():
        order = Order(user_id=current_user.id, ticket_id=ticket.id, quantity=form.quantity.data)
        ticket.available_tickets -= form.quantity.data
        db.session.add(order)
        db.session.commit()
        flash('Order placed successfully!', 'success')
        return redirect(url_for('tickets'))
    return render_template('order.html', form=form, ticket=ticket)

# 退出登录
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
