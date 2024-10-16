from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class Image(models.Model):
    id = models.AutoField(primary_key=True)
    path = models.ImageField(upload_to="img")
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    def __str__(self):
        return  str(self.id)

class CustomUserManager(UserManager):

    def _create_user(self, tg_id, password, **extra_fields):
        if not tg_id:
            raise ValueError("The tg_id field must be set.")
        user = self.model(tg_id=tg_id, **extra_fields)
        user.create_activation_code()
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, tg_id, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(tg_id, password, **extra_fields)

    def create_superuser(self, tg_id, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(tg_id, password, **extra_fields)


class CustomUser(AbstractUser):
    language_choices = (
        ("ru", "ru"),
        ("kg", "kg"),
        ("en", "en")
    )

    activation_code = models.CharField(max_length=60, blank=True)
    is_active = models.BooleanField(default=False)
    tg_id = models.IntegerField(unique=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    city_or_village = models.CharField(max_length=200, blank=True, null=True)
    school = models.CharField(max_length=100, blank=True, null=True)
    language = models.CharField(choices=language_choices, default="ru", max_length=2)
    avatar = models.ForeignKey(Image, on_delete=models.CASCADE, blank=True, null=True)
    username = models.CharField(max_length=50, blank=True, null=True)


    objects = CustomUserManager()
    USERNAME_FIELD = 'tg_id'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.tg_id}'

    def create_activation_code(self):
        import uuid
        code = str(uuid.uuid4())
        self.activation_code = code


