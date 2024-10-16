from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (QuizeChoiceModelViewSet, QuizeModelViewSet,
                    QuizeQuestionModelViewSet, QuizeTopicModelViewSet, QuizResultModelViewSet)

router = DefaultRouter()
router.register('question', QuizeQuestionModelViewSet)
router.register('topic', QuizeTopicModelViewSet)
router.register('choise', QuizeChoiceModelViewSet)
router.register('result', QuizResultModelViewSet)

router.register('', QuizeModelViewSet)


urlpatterns = [
    path('', include(router.urls)),
]

# urlpatterns += router.urls