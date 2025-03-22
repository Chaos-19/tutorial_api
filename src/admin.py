from django import forms
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.contenttypes.models import ContentType
from .models import Tutorial,Category,Course,Section,Lesson


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

# Register your models here.
@admin.register(Tutorial)
class TutorialAdmin(admin.ModelAdmin):
    list_display = ["title","img"]
    
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon','slug', 'tutorial']
    list_filter = [("tutorial",admin.RelatedOnlyFieldListFilter)]
    
    
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon','description', 'category','is_nested']
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
        
        print(len(nested_courses))
    
@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon','slug','description', 'course']
    list_filter = [("course",admin.RelatedOnlyFieldListFilter)]

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
    #list_filter = [("content_type",admin.RelatedOnlyFieldListFilter),("object_id",admin.RelatedOnlyFieldListFilter)]
    list_filter = [ParentFilter]
       