from django.db import models
from src.models import Tutorial,CloudinaryField

"""
class QuizCourse(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=200,unique=True)
    icon = CloudinaryField("image")
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE, related_name="quiz_courses")

    def __str__(self):
        return self.title
"""
class Quiz(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=200, unique=True)
    icon = CloudinaryField("image")
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE, related_name="quiz_courses")

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()  # "title" from data
    detail = models.TextField(blank=True)  # Optional detail
    output = models.TextField(blank=True)  # Full correct answer

    def __str__(self):
        return self.text

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    key = models.CharField(max_length=1)  # "a", "b", "c", "d"
    text = models.CharField(max_length=500)  # Option text
    is_correct = models.BooleanField(default=False)  # Marks the correct option

    def __str__(self):
        return f"{self.key}: {self.text}"