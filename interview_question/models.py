from django.db import models
from src.models import Tutorial,CloudinaryField


class Interview(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=200,unique=True)
    icon = CloudinaryField("image")
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE, related_name="interview_courses")

    def __str__(self):
        return self.title


class Question(models.Model):
    interview= models.ForeignKey(Interview, on_delete=models.CASCADE, related_name="questions")
    interview_question = models.CharField(max_length=500)
    answer = models.TextField(blank=True, default="")

    def __str__(self):
        return self.interview_question