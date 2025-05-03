from django.contrib import admin
from django.utils.html import format_html
from .models import QuizCourse, Quiz, Question, Option
from src.models import Tutorial
from tutorial_api.admin import CloudinaryAdminMixin  # Adjust path as needed

# Inlines
class QuizInline(admin.TabularInline):
    model = Quiz
    extra = 1
    fields = ['title']
    show_change_link = True

class OptionInline(admin.TabularInline):
    model = Option
    extra = 4  # Typically 4 options per question
    fields = ['key', 'text', 'is_correct']
    max_num = 4  # Limit to 4 options per question

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    fields = ['text', 'detail', 'output']
    show_change_link = True

# Admin Classes
@admin.register(QuizCourse)
class QuizCourseAdmin(CloudinaryAdminMixin, admin.ModelAdmin):
    cloudinary_fields = ['icon']
    list_display = ['title', 'image_preview', 'slug', 'tutorial']
    readonly_fields = ['image_preview']
    list_filter = [('tutorial', admin.RelatedOnlyFieldListFilter)]
    search_fields = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [QuizInline]
    list_per_page = 25

    def image_preview(self, obj):
        if obj.icon:
            return format_html(
                '<img src="{}" style="max-height: {}px; max-width: {}px; border-radius: 5px;" />',
                obj.icon.url,
                self.thumbnail_size,
                self.thumbnail_size
            )
        return "No image"
    image_preview.short_description = 'Preview'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('tutorial')

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'course']
    list_filter = [('course', admin.RelatedOnlyFieldListFilter), ('course__tutorial', admin.RelatedOnlyFieldListFilter)]
    search_fields = ['title']
    inlines = [QuestionInline]
    list_per_page = 25

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('course__tutorial')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text_preview', 'quiz', 'output_preview']
    list_filter = [('quiz', admin.RelatedOnlyFieldListFilter), ('quiz__course__tutorial', admin.RelatedOnlyFieldListFilter)]
    search_fields = ['text', 'output']
    inlines = [OptionInline]
    list_per_page = 25

    def text_preview(self, obj):
        return obj.text[:50] + ('...' if len(obj.text) > 50 else '')
    text_preview.short_description = 'Question'

    def output_preview(self, obj):
        return obj.output[:50] + ('...' if len(obj.output) > 50 else '')
    output_preview.short_description = 'Output'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('quiz__course')

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ['key', 'text_preview', 'is_correct', 'question']
    list_filter = [('question__quiz', admin.RelatedOnlyFieldListFilter), ('is_correct', admin.BooleanFieldListFilter)]
    search_fields = ['text']
    list_per_page = 25

    def text_preview(self, obj):
        return obj.text[:50] + ('...' if len(obj.text) > 50 else '')
    text_preview.short_description = 'Option Text'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('question__quiz')