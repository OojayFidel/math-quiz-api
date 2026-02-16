from django.urls import path
from .views import TopicListView, StartQuizView

urlpatterns = [
    path("topics/", TopicListView.as_view(), name="topics-list"),
    path("quizzes/start/", StartQuizView.as_view(), name="quiz-start"),
]
