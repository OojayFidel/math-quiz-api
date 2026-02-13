from django.urls import path
from .views import TopicListView

urlpatterns = [
    path("topics/", TopicListView.as_view(), name="topics-list"),
]
