# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.template import Context, loader
from django.core.mail import EmailMessage


def send_html_mail(subject, message, recipient_list):
    if not isinstance(recipient_list, list):
        recipient_list = [recipient_list]
    message = EmailMessage(subject, message, to=recipient_list)
    message.content_subtype = 'html'
    message.send()


def process_template(template, context):
    """ Обрабатывает шаблон, в котором первая строка считается заголовком """
    t = loader.get_template(template)
    c = Context(context)
    subject, content = t.render(c).split('\n', 1)
    return subject, content
