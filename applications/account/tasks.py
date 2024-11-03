from django.core.mail import send_mail
from config.celery import app


@app.task
def send_forgot_password_code(email, code):
    send_mail(
        'Extra theme py29',
        f'Вот ваш код для восстановления пароля, никому не показывайте его: {code}',
        'ort.tests.kg@gmail.com',
        [email]
    )