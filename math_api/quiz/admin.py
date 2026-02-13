from django.contrib import admin
from .models import Topic, Question, QuizSession, Attempt


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "topic", "difficulty", "question_text")
    list_filter = ("topic", "difficulty")
    search_fields = ("question_text",)


@admin.register(QuizSession)
class QuizSessionAdmin(admin.ModelAdmin):
    list_display = ("id", "student_identifier", "topic", "started_at", "completed_at", "score")
    list_filter = ("topic",)
    search_fields = ("student_identifier",)


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ("id", "quiz_session", "question", "is_correct", "timestamp")
    list_filter = ("is_correct", "timestamp")
