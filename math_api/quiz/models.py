from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    DIFFICULTY_CHOICES = (
        (1, "Easy"),
        (2, "Medium"),
        (3, "Hard"),
    )

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="questions")
    difficulty = models.PositiveSmallIntegerField(choices=DIFFICULTY_CHOICES, default=1)
    question_text = models.TextField()
    answer_choices = models.JSONField()
    correct_answer = models.CharField(max_length=255)
    explanation = models.TextField(blank=True)

    def __str__(self):
        return f"{self.topic.name} - {self.question_text[:50]}"


class QuizSession(models.Model):
    student_identifier = models.CharField(max_length=100)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="quiz_sessions")
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.student_identifier} - {self.topic.name}"


class Attempt(models.Model):
    quiz_session = models.ForeignKey(
        QuizSession, on_delete=models.CASCADE, related_name="attempts"
    )
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="attempts"
    )
    submitted_answer = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attempt {self.id}"
