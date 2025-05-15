from django.contrib import admin
from django.utils.html import format_html
from .models import Interview, Question
from src.models import Tutorial
from tutorial_api.admin import CloudinaryAdminMixin

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    fields = ['interview_question', 'answer']
    show_change_link = True

@admin.register(Interview)
class InterviewAdmin(CloudinaryAdminMixin, admin.ModelAdmin):
    cloudinary_fields = ['icon']
    list_display = ['title', 'image_preview', 'slug', 'tutorial']
    readonly_fields = ['image_preview']
    list_filter = [('tutorial', admin.RelatedOnlyFieldListFilter)]
    search_fields = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [QuestionInline]
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

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['interview_question_preview', 'interview', 'answer_preview']
    list_filter = [('interview', admin.RelatedOnlyFieldListFilter), ('interview__tutorial', admin.RelatedOnlyFieldListFilter)]
    search_fields = ['interview_question', 'answer']
    list_per_page = 25

    def interview_question_preview(self, obj):
        return obj.interview_question[:50] + ('...' if len(obj.interview_question) > 50 else '')
    interview_question_preview.short_description = 'Question'

    def answer_preview(self, obj):
        return obj.answer[:50] + ('...' if len(obj.answer) > 50 else '')
    answer_preview.short_description = 'Answer'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('interview__tutorial')