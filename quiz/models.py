from django.db import models
from src.models import Tutorial,CloudinaryField


class Quiz(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=200, unique=True)
    icon = CloudinaryField("image")
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE, related_name="quiz_courses")

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()
    detail_about = models.TextField(blank=True)
    output = models.TextField(blank=True)

    def __str__(self):
        return self.text

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    key = models.CharField(max_length=1)
    text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.key}: {self.text}"