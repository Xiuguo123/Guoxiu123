class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Completed')  # 新增的状态字段
    refund_requested = db.Column(db.Boolean, default=False)  # 是否申请退款
@app.route("/refund/<int:order_id>")
@login_required
def request_refund(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        flash('You cannot request a refund for this order', 'danger')
        return redirect(url_for('order_history'))
    
    order.refund_requested = True
    db.session.commit()
    flash('Refund request submitted', 'info')
    return redirect(url_for('order_history'))
