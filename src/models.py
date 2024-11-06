from django.db import models

# Create your models here.

class Tutorial(models.Model):
    img = models.CharField(max_length=300)
    title = models.CharField(max_length=300)
    
    
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
    content = models.TextField(blank=True,default="")

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons", null=True, blank=True)
    
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="section_lesson", null=True, blank=True)
    
    def related_entity(self):
        if self.course:
            return f"Course: {self.course.title}"
        elif self.section:
            return f"Nested Lesson: {self.section.title}"
        return "No related entity"

    def clean(self):
        if self.course and self.section:
            raise ValidationError("Lesson can only be related to either Course or Section, not both.")
        if not self.course and not self.section:
            raise ValidationError("Lesson must be related to either a Course or a Section.")

    def __str__(self):
        return f"{self.title}"
    
