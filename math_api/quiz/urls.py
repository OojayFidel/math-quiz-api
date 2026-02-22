from django.urls import path
from .views import TopicListView, StartQuizView
from .views import SubmitQuizView

urlpatterns = [
    path("topics/", TopicListView.as_view(), name="topics-list"),
    path("quizzes/start/", StartQuizView.as_view(), name="quiz-start"),
    path(
    "quizzes/<int:quiz_session_id>/submit/",
    SubmitQuizView.as_view(),
    name="quiz-submit",
),
]


