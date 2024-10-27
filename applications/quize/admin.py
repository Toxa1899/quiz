from django.contrib import admin

from applications.quize.models import (
    Quiz,
    QuizChoice,
    QuizQuestion,
    QuizTopic,
    QuizType,
    QuizResult,
)


class QuizChoiceModelAdmin(admin.TabularInline):
    model = QuizChoice


@admin.register(QuizQuestion)
class QuizQuestionAdminModel(admin.ModelAdmin):
    inlines = [QuizChoiceModelAdmin]


@admin.register(Quiz)
class QuizAdminModel(admin.ModelAdmin):
    list_display = ["title", "language"]


# Register your models here.
# admin.site.register(Quiz)
# admin.site.register(QuizQuestion)
admin.site.register(QuizTopic)
# admin.site.register(QuizChoice)
admin.site.register(QuizType)
admin.site.register(QuizResult)
