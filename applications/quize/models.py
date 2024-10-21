from django.contrib.auth import get_user_model
from django.db import models

from applications.account.models import Image


User = get_user_model()


class QuizType(models.Model):
    name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Название типа викторины",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Типы викторин"
        verbose_name_plural = "Типы викторин"


class Quiz(models.Model):
    language_choices = (("ru", "ru"), ("kg", "kg"), ("en", "en"))
    title = models.CharField(max_length=50, verbose_name="Название викторины")
    description = models.TextField(verbose_name="Описание викторины")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)
    is_published = models.BooleanField(
        default=False, verbose_name="Опубликована ли викторина"
    )
    language = models.CharField(
        choices=language_choices,
        default="ru",
        max_length=2,
        verbose_name="Язык викторины ru , en , kg",
    )
    image = models.ForeignKey(
        Image,
        on_delete=models.CASCADE,
        verbose_name="Внешний ключ на таблицу image(изображение)",
    )
    type = models.ForeignKey(
        QuizType,
        on_delete=models.CASCADE,
        verbose_name="Внешний ключ на таблицу quiz_type (Типы викторин)",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Викторина"
        verbose_name_plural = "Викторины"


class QuizTopic(models.Model):
    quiz_id = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        verbose_name="Внешний ключ на таблицу quiz_quiz (викторина)",
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название темы (например, "Математика", "История")',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Темы"
        verbose_name_plural = "Темы"


class QuizQuestion(models.Model):
    quiz_id = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        verbose_name="Внешний ключ на quiz_quiz (викторина)",
    )
    text = models.TextField(verbose_name="Текст вопроса")
    topic = models.ForeignKey(
        QuizTopic,
        on_delete=models.CASCADE,
        verbose_name="Внешний ключ на quiz_topic (Тема вопроса)",
    )
    image = models.ForeignKey(
        Image,
        on_delete=models.CASCADE,
        verbose_name="Внешний ключ на таблицу image(изображение)",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Вопросы"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return self.text


class QuizChoice(models.Model):
    question_id = models.ForeignKey(
        QuizQuestion,
        on_delete=models.CASCADE,
        verbose_name="Внешний ключ на quiz_question (вопрос)",
        related_name="choices",
    )
    text = models.TextField(verbose_name="Текст ответа")
    is_correct = models.BooleanField(
        default=False, verbose_name="Является ли ответ правильным"
    )
    image = models.ForeignKey(
        Image,
        on_delete=models.CASCADE,
        verbose_name="Внешний ключ на quiz_image (изображение) — необязательное поле",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Варианты ответа"
        verbose_name_plural = "Варианты ответа"

    def __str__(self):
        return self.text


class QuizResult(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Внешний ключ на пользователя",
    )
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        verbose_name="Внешний ключ на quiz_quiz (викторина)",
    )
    score = models.IntegerField(verbose_name="Количество набранных баллов")
    date_taken = models.DateTimeField(
        "Дата прохождения викторины", auto_now_add=True
    )

    class Meta:
        verbose_name = "Результаты тестов"
        verbose_name_plural = "Результаты тестов"
