class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 评分
    comment = db.Column(db.Text, nullable=False)  # 评论
    review_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(100), nullable=False)
    reviews = db.relationship('Review', backref='ticket', lazy=True)
class ReviewForm(FlaskForm):
    rating = IntegerField('Rating (1-5)', validators=[DataRequired(), NumberRange(min=1, max=5)])
    comment = StringField('Comment', validators=[DataRequired(), Length(max=200)])
    submit = SubmitField('Submit Review')
@app.route("/review/<int:ticket_id>", methods=['GET', 'POST'])
@login_required
def review(ticket_id):
    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(ticket_id=ticket_id, user_id=current_user.id, rating=form.rating.data, comment=form.comment.data)
        db.session.add(review)
        db.session.commit()
        flash('Review submitted successfully', 'success')
        return redirect(url_for('ticket', ticket_id=ticket_id))
    return render_template('review.html', form=form)
