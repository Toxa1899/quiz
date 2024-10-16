from rest_framework import serializers

from applications.account.models import Image
from applications.quize.models import (Quiz, QuizChoice, QuizQuestion,
                                       QuizResult, QuizTopic, QuizType)


class QuizTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizType
        fields = '__all__'


class QuizImage(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class ImageSerializerMixin(serializers.ModelSerializer):
    image = QuizImage(read_only=True)
    image_w = serializers.ImageField(write_only=True)


    def create_image_instance(self, validated_data):
        image_file = validated_data.pop('image_w')
        image = Image.objects.create(path=image_file)
        return image

    def create(self, validated_data):
        image = self.create_image_instance(validated_data)
        validated_data['image'] = image
        return super().create(validated_data)


class QuizSerializer(serializers.ModelSerializer):
    type = serializers.CharField(max_length=50, required=True)
    image = QuizImage(read_only=True)
    image_w = serializers.ImageField(write_only=True)

    class Meta:
        model = Quiz
        fields = [
            'id',
            'language',
            'title',
            'description',
            'is_published',
            'type',
            'image',
            'image_w'



        ]


    def create(self, validated_data):
        quiz_type_name = validated_data.pop('type')
        image_file = validated_data.pop('image_w')


        quiz_type, _ = QuizType.objects.get_or_create(name=quiz_type_name)


        image = Image.objects.create(path=image_file)
        validated_data['image'] = image
        validated_data['type'] = quiz_type
        quiz = Quiz.objects.create(**validated_data)


        return quiz



class QuizQuestionSerializer(ImageSerializerMixin):

    class Meta:
        model = QuizQuestion
        fields = '__all__'




class QuizTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizTopic
        fields = '__all__'

class QuizChoiceSerializer(ImageSerializerMixin):
    class Meta:
        model = QuizChoice
        fields = '__all__'


class QuizResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizResult
        fields = '__all__'

