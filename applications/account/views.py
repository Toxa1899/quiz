import hashlib
import hmac

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from django.views import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class TelegramLoginView(APIView):

    def get(self, request, *args, **kwargs):
        data = request.GET
        print(data)
        print('-------')
        return Response('succses')
        # auth_data = {
        #     'id': data.get('id'),
        #     'first_name': data.get('first_name'),
        #     'last_name': data.get('last_name'),
        #     'username': data.get('username'),
        #     'photo_url': data.get('photo_url'),
        #     'auth_date': data.get('auth_date'),
        #     'hash': data.get('hash')
        # }

      
        # user, created = User.objects.get_or_create(tg_id=auth_data['id'], defaults={
        #     'tg_id': auth_data["id"],
        #     'username': auth_data['username'] ,
        #     'password': make_password(auth_data['hash'])

        # })


        # refresh = RefreshToken.for_user(user)
        # access_token = str(refresh.access_token)
        # refresh_token = str(refresh)

        # # Возврат токенов
        # return Response({
        #     'access': access_token,
        #     'refresh': refresh_token
        # })

def tg(requests):
    return  render(requests, 'index.html')


