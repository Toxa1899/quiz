from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.shortcuts import render
import hashlib
import hmac
from decouple import  config
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
User = get_user_model()



BOT_TOKEN = config('BOT_TOKEN')

def check_telegram_authorization(auth_data):
    # Извлекаем хэш и удаляем его из данных
    check_hash = auth_data.pop('hash', None)

    # Генерация строки проверки
    data_check_arr = [f"{key}={value}" for key, value in auth_data.items()]
    data_check_arr.sort()  # Сортировка
    data_check_string = "\n".join(data_check_arr)

    # Генерация секретного ключа
    secret_key = hashlib.sha256(BOT_TOKEN.encode()).digest()

    # Генерация HMAC
    hash_value = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).digest()

    # Сравнение хэшей
    if not hmac.compare_digest(hash_value, bytes.fromhex(check_hash)):
        return 'Data is NOT from Telegram'

    user, created = User.objects.get_or_create(tg_id=auth_data['id'], defaults={
        'tg_id': auth_data["id"],
        'username': auth_data['username'] ,
        'password': make_password(check_hash)

    })

    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    # Возврат токенов
    return {
        'access': access_token,
        'refresh': refresh_token
    }

    # return 'success'


class TelegramLoginView(APIView):

    def post(self, request, *args, **kwargs):
        data = request.data
        tg = check_telegram_authorization(data)
        print(tg)

        return Response(tg)

    def get(self, request, *args, **kwargs):
        data_get = request.GET

        data = {
            'id' : data_get['id'],
            'first_name' : data_get['first_name'],
            'username' : data_get['username'],
            'photo_url' : data_get['photo_url'],
            'auth_date' : data_get['auth_date'],
            'hash': data_get['hash'],


        }





        tg = check_telegram_authorization(data)

        return Response(tg)


def tg(requests):
    return  render(requests, 'index.html')


