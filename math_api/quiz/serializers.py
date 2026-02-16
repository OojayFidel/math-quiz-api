from rest_framework import serializers
from .models import Topic, Question


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ["id", "name", "description"]


class StartQuizSerializer(serializers.Serializer):
    student_identifier = serializers.CharField(max_length=100)
    topic_id = serializers.IntegerField()


class QuestionPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        # Do NOT expose correct_answer
        fields = ["id", "topic", "difficulty", "question_text", "answer_choices"]
