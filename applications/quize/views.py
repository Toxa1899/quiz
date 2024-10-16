from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from applications.quize.models import (Quiz, QuizChoice, QuizQuestion,
                                       QuizResult, QuizTopic)
from applications.quize.serializers import (QuizChoiceSerializer,
                                            QuizQuestionSerializer,
                                            QuizResultSerializer,
                                            QuizSerializer,
                                            QuizTopicSerializer)


class QuizeModelViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    # permission_classes = [IsAuthenticated]

    # def list(self, request, *args, **kwargs):
    #     queryset = Quiz.objects.all()
    #     serializer = QuizSerializer(queryset, many=True)
    #
    #     return  Response(serializer.data)
    #



class QuizeQuestionModelViewSet(viewsets.ModelViewSet):
    queryset = QuizQuestion.objects.all()
    serializer_class = QuizQuestionSerializer


class QuizeTopicModelViewSet(viewsets.ModelViewSet):
    queryset = QuizTopic.objects.all()
    serializer_class = QuizTopicSerializer


class QuizeChoiceModelViewSet(viewsets.ModelViewSet):
    queryset = QuizChoice.objects.all()
    serializer_class = QuizChoiceSerializer

class QuizResultModelViewSet(viewsets.ModelViewSet):
    queryset = QuizResult.objects.all()
    serializer_class = QuizResultSerializer