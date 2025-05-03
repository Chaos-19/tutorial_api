# project_name/utils/admin.py
from cloudinary import uploader
from django.utils.html import format_html

class CloudinaryAdminMixin:
    cloudinary_fields = []
    thumbnail_size = 50

    def save_model(self, request, obj, form, change):
        if change:
            original = self.model.objects.get(pk=obj.pk)
            for field in self.cloudinary_fields:
                original_image = getattr(original, field)
                new_image = getattr(obj, field)
                if original_image and original_image != new_image:
                    try:
                        uploader.destroy(original_image.public_id)
                    except Exception as e:
                        print(f"Error deleting old {field}: {e}")
        super().save_model(request, obj, form, change)

    def delete_cloudinary_images(self, instance):
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
        if self.cloudinary_fields:
            first_field = getattr(obj, self.cloudinary_fields[0])
            if first_field:
                return format_html(
                    '<img src="{}" style="max-height: {}px; max-width: {}px; border-radius: 5px;" />',
                    first_field.url,
                    self.thumbnail_size,
                    self.thumbnail_size
                )
        return "No image"
    image_preview.short_description = 'Preview'