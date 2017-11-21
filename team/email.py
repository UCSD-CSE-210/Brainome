import os

from flask import render_template
from flask_mail import Message
from . import mail


def send_email(recipient, subject, template, **kwargs):
        msg = Message(
            'Email' + ' ' + subject,
            sender='kuppal2790@gmail.com',
            recipients=[recipient])
        msg.body = render_template(template + '.txt', **kwargs)
        msg.html = render_template(template + '.html', **kwargs)
        mail.send(msg)
