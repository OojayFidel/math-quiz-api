from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Topic, Question, QuizSession
from .serializers import TopicSerializer, StartQuizSerializer, QuestionPublicSerializer


class TopicListView(APIView):
    def get(self, request):
        topics = Topic.objects.all()
        return Response(TopicSerializer(topics, many=True).data, status=status.HTTP_200_OK)


class StartQuizView(APIView):
    def post(self, request):
        payload = StartQuizSerializer(data=request.data)
        payload.is_valid(raise_exception=True)

        student_identifier = payload.validated_data["student_identifier"]
        topic_id = payload.validated_data["topic_id"]

        try:
            topic = Topic.objects.get(id=topic_id)
        except Topic.DoesNotExist:
            return Response({"error": "Topic not found."}, status=status.HTTP_404_NOT_FOUND)

        questions = Question.objects.filter(topic=topic).order_by("?")[:5]
        if questions.count() < 5:
            return Response(
                {"error": "Not enough questions for this topic. Add at least 5."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        session = QuizSession.objects.create(student_identifier=student_identifier, topic=topic)

        return Response(
            {
                "quiz_session_id": session.id,
                "topic": {"id": topic.id, "name": topic.name},
                "questions": QuestionPublicSerializer(questions, many=True).data,
            },
            status=status.HTTP_201_CREATED,
        )
    
from django.utils import timezone
from .models import Attempt
from .serializers import SubmitQuizSerializer

class SubmitQuizView(APIView):
    def post(self, request, quiz_session_id):
        # Validate session
        try:
            session = QuizSession.objects.get(id=quiz_session_id)
        except QuizSession.DoesNotExist:
            return Response(
                {"error": "Quiz session not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Prevent double submission
        if session.completed_at:
            return Response(
                {"error": "Quiz already submitted."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = SubmitQuizSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        answers = serializer.validated_data["answers"]

        score = 0
        total_questions = len(answers)

        for answer in answers:
            try:
                question = Question.objects.get(id=answer["question_id"])
            except Question.DoesNotExist:
                continue

            is_correct = question.correct_answer == answer["submitted_answer"]

            if is_correct:
                score += 1

            Attempt.objects.create(
                quiz_session=session,
                question=question,
                submitted_answer=answer["submitted_answer"],
                is_correct=is_correct,
            )

        session.score = score
        session.completed_at = timezone.now()
        session.save()

        percentage = (score / total_questions) * 100 if total_questions > 0 else 0

        return Response(
            {
                "score": score,
                "total_questions": total_questions,
                "percentage": percentage,
            },
            status=status.HTTP_200_OK,
        )


from django.db.models import Count, Sum
from .models import Attempt


class StudentProgressView(APIView):
    def get(self, request, student_identifier):
        sessions = QuizSession.objects.filter(
            student_identifier=student_identifier,
            completed_at__isnull=False
        )

        if not sessions.exists():
            return Response(
                {"student_identifier": student_identifier, "topics": []},
                status=status.HTTP_200_OK
            )

        attempts = Attempt.objects.filter(quiz_session__in=sessions)

        topic_stats = (
            attempts
            .values("question__topic__name")
            .annotate(
                total_attempts=Count("id"),
                correct_attempts=Sum("is_correct")
            )
        )

        topics_data = []

        for stat in topic_stats:
            total = stat["total_attempts"]
            correct = stat["correct_attempts"] or 0
            accuracy = (correct / total) * 100 if total > 0 else 0

            topics_data.append({
                "topic": stat["question__topic__name"],
                "total_attempts": total,
                "accuracy_percentage": round(accuracy, 2)
            })

        return Response(
            {
                "student_identifier": student_identifier,
                "topics": topics_data
            },
            status=status.HTTP_200_OK
        )