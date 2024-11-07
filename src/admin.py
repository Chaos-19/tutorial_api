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
    content_object = forms.ModelChoiceField(
        queryset=None,
        required=False,
        label="Related Object"
    )
    
    class Meta:
        model = Lesson
        fields = ['title', 'content', 'content_object']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get content type for Course and Section
        course_type = ContentType.objects.get_for_model(Course)
        section_type = ContentType.objects.get_for_model(Section)
        
        # Combine Course and Section querysets to use as choices in `content_object`
        self.fields['content_object'].queryset = Course.objects.all() | Section.objects.all()
        
        if self.instance.pk:
            if self.instance.content_type == course_type:
                self.fields['content_object'].initial = Course.objects.get(pk=self.instance.object_id)
            elif self.instance.content_type == section_type:
                self.fields['content_object'].initial = Section.objects.get(pk=self.instance.object_id)
    
    def save(self, commit=True):
        content_object = self.cleaned_data['content_object']
        if content_object:
            self.instance.content_type = ContentType.objects.get_for_model(content_object)
            self.instance.object_id = content_object.id
        return super().save(commit)
  

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    form = LessonAdminForm
    list_display = ['title', 'content','object_id', 'content_type','parent']
    
    
