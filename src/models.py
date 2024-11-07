from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.
class Tutorial(models.Model):
    img = models.CharField(max_length=300)
    title = models.CharField(max_length=300)
    
    def __str__(self):
      return self.title
    
    
class Category(models.Model):
    name = models.CharField(max_length=300)
    icon = models.CharField(max_length=1000)
    slug = models.SlugField(max_length=200, unique=True)
    
    tutorial = models.ForeignKey(Tutorial,on_delete=models.CASCADE, related_name="tutorial")
    
    def __str__(self):
      return f"{self.name}"

class Course(models.Model):
    title = models.CharField(max_length=300)
    icon = models.CharField(max_length=100)
    description = models.TextField(blank=True,default="")
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="courses")
    
    def __str__(self):
      return f"{self.title}"
      

class Section(models.Model):
    title = models.CharField(max_length=300)
    icon = models.CharField(max_length=1000)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField( blank=True, default="")
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lesson_section")
    
    def __str__(self):
      return f"{self.title}"

class Lesson(models.Model):
    title = models.CharField(max_length=300)
    content = models.TextField(blank=True, default="")
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,null=True)
    object_id = models.PositiveIntegerField(null=True)
    parent = GenericForeignKey('content_type', 'object_id')
    
    def __str__(self):
        return self.title
  