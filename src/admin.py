from django import forms
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.contenttypes.models import ContentType
from .models import Tutorial,Category,Course,Section,Lesson

# Register your models here.
@admin.register(Tutorial)
class TutorialAdmin(admin.ModelAdmin):
    list_display = ["img","title"]
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon','slug', 'tutorial']
    
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon','description', 'category']
    
@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon','slug','description', 'course']


# Step 1: Create a custom form for Lesson
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