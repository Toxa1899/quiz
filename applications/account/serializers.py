import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import ValidationError
from .models import CustomUser, Image
from .tasks import send_forgot_password_code
User = get_user_model()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RegisterSerializers(serializers.ModelSerializer):
    password2 = serializers.CharField(
        min_length=8, required=True, write_only=True
    )

    class Meta:
        model = User
        fields = ("email", "password", "password2")

    def validate(self, attrs):
        p1 = attrs.get("password")
        p2 = attrs.pop("password2")

        if p1 != p2:
            raise serializers.ValidationError("Пароли не совпадают")

        try:
            validate_password(p1)
        except ValidationError as e:
            raise serializers.ValidationError({list(e.messages)})

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class DeleteAccountSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, write_only=True)


class ChangePasswordSerializers(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
    new_password_confirm = serializers.CharField(required=True, min_length=8)

    def validate_old_password(self, password):
        user = self.context["request"].user
        if not user.check_password(password):
            logger.warning(
                f"Неудачная попытка смены пароля для пользователя '{user.email}'. Неправильный старый пароль."
            )
            raise serializers.ValidationError("Пароль не совпадает с текущим")
        return password

    def validate(self, attrs):
        new_password = attrs.get("new_password")
        new_password_confirm = attrs.get("new_password_confirm")
        user = self.context["request"].user

        if new_password != new_password_confirm:
            logger.warning(
                f"Неудачная попытка смены пароля для пользователя '{user.email}'. Пароли не совпадают"
            )
            raise serializers.ValidationError("Пароли не совпадают")

        if user.check_password(new_password):
            logger.warning(
                f"Неудачная попытка смены пароля для пользователя '{user.email}'. Новый пароль совпадает с текущим"
            )
            raise serializers.ValidationError(
                "Новый пароль совпадает с текущим"
            )

        try:
            validate_password(new_password)
        except ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return attrs

    def set_new_password(self):
        user = self.context["request"].user
        new_password = self.validated_data["new_password"]
        user.set_password(new_password)
        user.save(update_fields=["password"])
        logger.info(f"Пароль для пользователя '{user.email}' был изменён")




class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    img_data = ImageSerializer(
            source="img", read_only=True
        )

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "last_login",
            "last_name",
            "first_name",
            "img",
            "email",
            "img_data"
            
        ]

class ForgotPasswordSerializers(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь с такой почтой не найден ')
        return email

    def send_code(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.create_activation_code()
        user.save()
        send_forgot_password_code.delay(user.email, user.activation_code)


class ForgotPasswordConfirmSerializers(serializers.Serializer):
    code = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=6)
    new_password_confirm = serializers.CharField(required=True, min_length=6)

    @staticmethod
    def validate_code(code):
        if not User.objects.filter(activation_code=code).exists():
            raise serializers.ValidationError('Неверный код')
        return code

    def validate(self, attrs):
        p1 = attrs.get('new_password')
        p2 = attrs.get('new_password_confirm')

        if p1 != p2:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def set_new_password(self):
        code = self.validated_data.get('code')
        password = self._validated_data.get('new_password')
        user = User.objects.get(activation_code=code)
        user.set_password(password)
        user.activation_code = ''
        user.save(update_fields=['password', 'activation_code'])