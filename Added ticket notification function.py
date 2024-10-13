pip install Flask-Mail
from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

# 配置邮件服务
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-password'
mail = Mail(app)

# 发送邮件通知功能
def send_ticket_confirmation(user_email, event_name):
    msg = Message('Ticket Confirmation', 
                  sender='your-email@gmail.com', 
                  recipients=[user_email])
    msg.body = f'Thank you for purchasing tickets for {event_name}. Enjoy the event!'
    mail.send(msg)

@app.route("/buy_ticket/<int:ticket_id>")
def buy_ticket(ticket_id):
    # 假设已经处理了购票逻辑，获取了用户和事件信息
    user_email = "user@example.com"
    event_name = "Concert 2024"
    send_ticket_confirmation(user_email, event_name)
    return "Ticket purchase complete. Confirmation email sent!"
