from django.contrib import admin

from applications.quize.models import Quiz, QuizChoice, QuizQuestion, QuizTopic

# Register your models here.
admin.site.register(Quiz)
admin.site.register(QuizQuestion)
admin.site.register(QuizTopic)
admin.site.register(QuizChoice)