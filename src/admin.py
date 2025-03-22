from django import forms
from django.contrib import admin
from django.utils.html import format_html
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.contenttypes.models import ContentType
from .models import Tutorial,Category,Course,Section,Lesson

from cloudinary import uploader


class ParentFilter(admin.SimpleListFilter):
    title = 'Parent'
    parameter_name = 'parent'

    def lookups(self, request, model_admin):
        # Get all possible parent objects
        courses = Course.objects.all()
        sections = Section.objects.all()
        
        # Create filter options
        return [
            *[('course-%d' % c.id, f'Course: {c.title}') for c in courses],
            *[('section-%d' % s.id, f'Section: {s.title}') for s in sections],
        ]

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
            
        # Split the value into model type and ID
        model_type, obj_id = self.value().split('-')
        content_type = ContentType.objects.get(model=model_type)
        return queryset.filter(
            content_type=content_type,
            object_id=obj_id
        )

class CloudinaryAdminMixin:
    cloudinary_fields = []  # Override this in child classes with field names
    thumbnail_size = 50  # Default thumbnail size in pixels
    
    def save_model(self, request, obj, form, change):
        # Handle image updates
        if change:  # Only for existing objects
            original = self.model.objects.get(pk=obj.pk)
            for field in self.cloudinary_fields:
                original_image = getattr(original, field)
                new_image = getattr(obj, field)
                
                # Delete old image if it's being changed or removed
                if original_image and original_image != new_image:
                    try:
                        uploader.destroy(original_image.public_id)
                    except Exception as e:
                        print(f"Error deleting old {field}: {e}")

        super().save_model(request, obj, form, change)

    def delete_cloudinary_images(self, instance):
        """Delete all Cloudinary images associated with the instance"""
        for field_name in self.cloudinary_fields:
            if hasattr(instance, field_name):
                field = getattr(instance, field_name)
                if field:
                    try:
                        uploader.destroy(field.public_id)
                    except Exception as e:
                        print(f"Error deleting {field_name}: {e}")

    def delete_model(self, request, obj):
        self.delete_cloudinary_images(obj)
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            self.delete_cloudinary_images(obj)
        super().delete_queryset(request, queryset)

    def image_preview(self, obj):
        """Generate thumbnail preview for first Cloudinary field"""
        if self.cloudinary_fields:
            first_field = getattr(obj, self.cloudinary_fields[0])
            if first_field:
                return format_html(
                    # Fix: Use consistent positional parameters
                    '<img src="{0}" style="max-height: {1}px; max-width: {1}px;border-radius: 5px;" />',
                    first_field.url,
                    self.thumbnail_size
                )
        return "No image"
    image_preview.short_description = 'Preview'

# Register your models here.
@admin.register(Tutorial)
class TutorialAdmin(CloudinaryAdminMixin,admin.ModelAdmin):
    cloudinary_fields = ['img']
    list_display = ["title", "image_preview"]
    readonly_fields = ['image_preview']

@admin.register(Category)
class CategoryAdmin(CloudinaryAdminMixin,admin.ModelAdmin):
    cloudinary_fields = ['icon']
    list_display = ['name', 'image_preview', 'slug', 'tutorial']
    readonly_fields = ['image_preview']
    list_filter = [("tutorial",admin.RelatedOnlyFieldListFilter)]
    
@admin.register(Course)
class CourseAdmin(CloudinaryAdminMixin,admin.ModelAdmin):
    cloudinary_fields = ['icon']
    list_display = ['title', 'image_preview','description', 'category','is_nested']
    readonly_fields = ['image_preview']
    list_filter = [("category",admin.RelatedOnlyFieldListFilter)]
    actions = ['update_is_nested']
    
    def update_is_nested(self, request, queryset):
        section_content_type = ContentType.objects.get(model="section")
        lessons = Lesson.objects.filter(content_type=section_content_type)
        
        nested_courses = Course.objects.filter(
          id__in=Section.objects.filter(
            id__in=Lesson.objects.filter(content_type=section_content_type).values_list('object_id', flat=True)
          ).values_list('course_id', flat=True)
        )
        
        #print(len(nested_courses))
    
@admin.register(Section)
class SectionAdmin(CloudinaryAdminMixin,admin.ModelAdmin):
    cloudinary_fields = ['icon']
    list_display = ['title', 'image_preview','slug','description', 'course']
    readonly_fields = ['image_preview']
    list_filter = [("course",admin.RelatedOnlyFieldListFilter)]


class LessonAdminForm(forms.ModelForm):
    content_object = forms.ChoiceField(
        choices=[],
        required=False,
        label="Related Object"
    )
    
    class Meta:
        model = Lesson
        fields = ['title', 'content', 'content_object']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Get all Course and Section items, prepending labels to show which model they belong to
        course_choices = [(f"course-{course.id}", f"Course: {course.title}") for course in Course.objects.all()]
        section_choices = [(f"section-{section.id}", f"Section: {section.title}") for section in Section.objects.all()]
        
        # Set choices in the content_object field
        self.fields['content_object'].choices = [("", "Select related object")] + course_choices + section_choices
        
        # Preselect the current related object, if it exists
        if self.instance.pk:
            if self.instance.content_type.model == 'course':
                self.fields['content_object'].initial = f"course-{self.instance.object_id}"
            elif self.instance.content_type.model == 'section':
                self.fields['content_object'].initial = f"section-{self.instance.object_id}"

    def save(self, commit=True):
        content_object = self.cleaned_data['content_object']
        if content_object:
            # Split choice value into type and ID
            object_type, object_id = content_object.split("-")
            if object_type == "course":
                self.instance.content_type = ContentType.objects.get_for_model(Course)
            elif object_type == "section":
                self.instance.content_type = ContentType.objects.get_for_model(Section)
            self.instance.object_id = object_id
        return super().save(commit)
  

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    form = LessonAdminForm
    list_display = ['title', 'content','object_id', 'content_type','parent']
    list_filter = [ParentFilter]