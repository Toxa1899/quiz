from django.contrib.admin.templatetags.admin_list import pagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    DjangoModelPermissionsOrAnonReadOnly,
)
from rest_framework.response import Response
from urllib3 import request

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
from django.db.models import Max

from django.db.models import OuterRef, Subquery
from django_filters import rest_framework as filters


from drf_yasg import openapi
from .permissions import IsAuthorOrReadOnly

class QuizFilter(filters.FilterSet):
    type = filters.CharFilter(field_name="type__name")

    class Meta:
        model = Quiz
        fields = ["language", "type"]


class QuizeModelViewSet(viewsets.ModelViewSet):
    permission_classes = [
        DjangoModelPermissionsOrAnonReadOnly,
        IsAuthenticatedOrReadOnly,
    ]
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = QuizFilter


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

class QuizResultFilter(filters.FilterSet):
    size = filters.NumberFilter(field_name='size', method='filter_by_page_size')

    class Meta:
        model = QuizResult
        fields = ['quiz__id']

    def filter_by_page_size(self, queryset, name, value):
        return queryset[:value]




# @method_decorator(
#     name="list", decorator=swagger_auto_schema(manual_parameters=params)
# )
class QuizResultModelViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsAuthenticated,
        IsAuthorOrReadOnly
    ]
    queryset = QuizResult.objects.all()
    serializer_class = QuizResultSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = QuizResultFilter



    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        # page_size = self.request.query_params.get('size', None)
        # print(self.request.query_params)
        # if page_size:
        #     queryset = queryset[:int(page_size)]
        return queryset


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)







class QuizResulAlltAPIView(APIView):

    def get(self, request):
        max_scores = QuizResult.objects.values('user_id').annotate(max_score=Max('score')).values('max_score')

        queryset = QuizResult.objects.filter(
            score=Subquery(max_scores.filter(user_id=OuterRef('user_id')))
        )
        serializer = QuizResultSerializer(queryset, many=True)
        return Response(serializer.data)
