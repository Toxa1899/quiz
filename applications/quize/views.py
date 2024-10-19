from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    DjangoModelPermissionsOrAnonReadOnly
)
from rest_framework.response import Response

from applications.quize.models import (
    Quiz,
    QuizChoice,
    QuizQuestion,
    QuizResult,
    QuizTopic,
)
from applications.quize.serializers import (
    QuizChoiceSerializer,
    QuizQuestionSerializer,
    QuizResultSerializer,
    QuizSerializer,
    QuizTopicSerializer,
)


class QuizeModelViewSet(viewsets.ModelViewSet):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["language"]

    def get_queryset(self):
        queryset = super().get_queryset()
        # language = self.request.query_params.get('language')
        quiz_type = self.request.query_params.get("type")

        # if language:
        #     queryset = queryset.filter(language=language)

        if quiz_type:
            queryset = queryset.filter(type__name=quiz_type)

        return queryset


class QuizeQuestionModelViewSet(viewsets.ModelViewSet):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    queryset = QuizQuestion.objects.all()
    serializer_class = QuizQuestionSerializer


class QuizeTopicModelViewSet(viewsets.ModelViewSet):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    queryset = QuizTopic.objects.all()
    serializer_class = QuizTopicSerializer


class QuizeChoiceModelViewSet(viewsets.ModelViewSet):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    queryset = QuizChoice.objects.all()
    serializer_class = QuizChoiceSerializer


class QuizResultModelViewSet(viewsets.ModelViewSet):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    queryset = QuizResult.objects.all()
    serializer_class = QuizResultSerializer
