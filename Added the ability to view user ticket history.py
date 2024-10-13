class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Completed')  # 状态字段

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    orders = db.relationship('Order', backref='customer', lazy=True)
@app.route("/history")
@login_required
def order_history():
    orders = Order.query.filter_by(user_id=current_user.id).all()
    return render_template('history.html', orders=orders)
<h1>Your Ticket Purchase History</h1>
{% for order in orders %}
    <p>Event: {{ order.ticket.event_name }} | Quantity: {{ order.quantity }} | Date: {{ order.order_date }}</p>
{% endfor %}
