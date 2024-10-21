from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    DjangoModelPermissionsOrAnonReadOnly,
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


from django_filters import rest_framework as filters


class QuizFilter(filters.FilterSet):
    type = filters.CharFilter(field_name="type__name")

    class Meta:
        model = Quiz
        fields = ["language", "type"]


class QuizeModelViewSet(viewsets.ModelViewSet):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = QuizFilter

    # def get_queryset(self):
    #     queryset = super().get_queryset()

    #     quiz_type = self.request.query_params.get("type")

    #     if quiz_type:
    #         queryset = queryset.filter(type__name=quiz_type)

    #     return queryset


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
