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
from django.utils.decorators import method_decorator


from django_filters import rest_framework as filters
from .decorators import rating_schema
from rest_framework import status
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class QuizFilter(filters.FilterSet):
    type = filters.CharFilter(field_name="type__name")

    class Meta:
        model = Quiz
        fields = ["language", "type"]


class QuizeModelViewSet(viewsets.ModelViewSet):
    permission_classes = [
        DjangoModelPermissionsOrAnonReadOnly,
        IsAuthenticated,
    ]
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
    permission_classes = [
        DjangoModelPermissionsOrAnonReadOnly,
        IsAuthenticated,
    ]
    queryset = QuizQuestion.objects.all()
    serializer_class = QuizQuestionSerializer


class QuizeTopicModelViewSet(viewsets.ModelViewSet):
    permission_classes = [
        DjangoModelPermissionsOrAnonReadOnly,
        IsAuthenticated,
    ]
    queryset = QuizTopic.objects.all()
    serializer_class = QuizTopicSerializer


class QuizeChoiceModelViewSet(viewsets.ModelViewSet):
    permission_classes = [
        DjangoModelPermissionsOrAnonReadOnly,
        IsAuthenticated,
    ]
    queryset = QuizChoice.objects.all()
    serializer_class = QuizChoiceSerializer


params = [
    openapi.Parameter(
        "size",
        openapi.IN_PATH,
        description="количество результатов",
        type=openapi.TYPE_INTEGER,
    )
]


@method_decorator(
    name="list", decorator=swagger_auto_schema(manual_parameters=params)
)
class QuizResultModelViewSet(viewsets.ModelViewSet):
    permission_classes = [
        DjangoModelPermissionsOrAnonReadOnly,
        IsAuthenticated,
    ]
    queryset = QuizResult.objects.all()
    serializer_class = QuizResultSerializer

    def list(self, request):
        """
        size -- количество результатов
        """
        query_params = self.request.query_params
        size = (
            int(query_params.get("size", None))
            if query_params.get("size", None)
            else None
        )
        result = QuizResult.objects.all()[:size]
        serializer = QuizResultSerializer(result, many=True)
        return Response(serializer.data)
