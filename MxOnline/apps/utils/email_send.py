# -*- coding: utf-8 -*-
__author__ = 'Eric'
__date__ = '2018/2/20 19:50'

from random import Random

from users.models import EmailVerifyRecord
from django.core.mail import send_mail

from MxOnline.settings import EMAIL_FROM


def generate_random_str(random_length=8):
    """

    :param random_length: 随机数长度
    :return: 随机字符
    """
    str = ''
    chars = 'ABCDEFGabcdefgHIGKLMNhigklmn1234567890OPQRSTUVWXYZopqrstuvwxyz'
    length = len(chars) - 1
    random  = Random()
    for i in range(random_length):
        str += chars[random.randint(0, length)]
    return  str



def send_verify_code(email, sent_type='register'):
    email_record = EmailVerifyRecord()
    code = generate_random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.sent_type = sent_type
    email_record.save()

    email_title = ''
    email_body =  ''

    if sent_type == 'register':
        email_title = '慕学在线网注册激活链接'
        email_body = '请点击下面的链接激活你的账号：http://127.0.0.1:8000/active/{0}'.format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass



    if sent_type == 'forget':
        email_title = '慕学在线网重置密码链接'
        email_body = '请点击下面的链接重置你的密码：http://127.0.0.1:8000/reset/{0}'.format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass


