class AddTicketForm(FlaskForm):
    event_name = StringField('Event Name', validators=[DataRequired(), Length(min=2, max=100)])
    event_date = StringField('Event Date (YYYY-MM-DD)', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0.01, message="Price must be greater than zero")])
    available_tickets = IntegerField('Available Tickets', validators=[DataRequired(), NumberRange(min=1, message="Must have at least 1 ticket")])
    submit = SubmitField('Add Ticket')
