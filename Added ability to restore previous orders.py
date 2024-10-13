class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Completed')  # 订单状态
    is_deleted = db.Column(db.Boolean, default=False)  # 新增的软删除字段
@app.route("/cancel_order/<int:order_id>")
@login_required
def cancel_order(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        flash('You cannot cancel this order', 'danger')
        return redirect(url_for('order_history'))
    
    order.is_deleted = True  # 标记订单为已删除
    db.session.commit()
    flash('Order cancelled', 'info')
    return redirect(url_for('order_history'))

@app.route("/deleted_orders")
@login_required
def deleted_orders():
    orders = Order.query.filter_by(user_id=current_user.id, is_deleted=True).all()
    return render_template('deleted_orders.html', orders=orders)

@app.route("/recover_order/<int:order_id>")
@login_required
def recover_order(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        flash('You cannot recover this order', 'danger')
        return redirect(url_for('deleted_orders'))
    
    order.is_deleted = False  # 恢复订单
    db.session.commit()
    flash('Order recovered', 'success')
    return redirect(url_for('order_history'))
<h1>Your Deleted Orders</h1>
{% for order in orders %}
    <p>Event: {{ order.ticket.event_name }} | Quantity: {{ order.quantity }} | Date: {{ order.order_date }}
        <a href="{{ url_for('recover_order', order_id=order.id) }}">Recover</a>
    </p>
{% endfor %}
