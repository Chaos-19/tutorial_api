from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey,GenericRelation
from django.contrib.contenttypes.models import ContentType

import cloudinary.uploader
from cloudinary.models import CloudinaryField as BaseCloudinaryField 



class CloudinaryField(BaseCloudinaryField):
    def upload_options(self, model_instance):
        return {
            'public_id': f"{model_instance._meta.model_name}-{model_instance.id}",
            'unique_filename': False,
            'overwrite': True,
            'resource_type': 'image',
            #'tags': ['map', 'market-map'],
            'invalidate': True,
            'quality': 'auto:eco',
        }


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Tutorial(TimestampedModel):
    title = models.CharField(max_length=300)
    img = CloudinaryField("image")
    
    def __str__(self):
        return self.title

class Category(TimestampedModel):
    name = models.CharField(max_length=300)
    icon = CloudinaryField("image")
    #icon = models.URLField(max_length=1000, help_text="URL of the category icon")
    slug = models.SlugField(max_length=200, unique=True)
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE, related_name="categories")

    def __str__(self):
        return self.name
        
class Lesson(TimestampedModel):
    title = models.CharField(max_length=300)
    content = models.TextField(blank=True, default="")

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    parent = GenericForeignKey('content_type', 'object_id')

class Course(TimestampedModel):
    title = models.CharField(max_length=300)
    icon = CloudinaryField("image")
    #icon = models.URLField(max_length=300, help_text="URL of the course icon")
    description = models.TextField(blank=True, default="")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="courses")
    is_nested = models.BooleanField(default=False)
    
    lessons = GenericRelation(
        Lesson,
        content_type_field='content_type',
        object_id_field='object_id',
        related_query_name='courses'
    )

    def __str__(self):
        return self.title

class Section(TimestampedModel):
    title = models.CharField(max_length=300)
    icon = CloudinaryField("image")
    #icon = models.URLField(max_length=1000, help_text="URL of the section icon")
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True, default="")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="sections")
    
    lessons = GenericRelation(
        Lesson,
        content_type_field='content_type',
        object_id_field='object_id',
        related_query_name='sections'
    )

    def __str__(self):
        return self.title


    '''

    def __str__(self):
        return self'''