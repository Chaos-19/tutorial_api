# Generated by Django 5.1.3 on 2024-11-08 09:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0002_remove_lesson_course_remove_lesson_section_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='category',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='course',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='course',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='lesson',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='lesson',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='section',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='section',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='tutorial',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='tutorial',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='icon',
            field=models.URLField(help_text='URL of the category icon', max_length=1000),
        ),
        migrations.AlterField(
            model_name='category',
            name='tutorial',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='src.tutorial'),
        ),
        migrations.AlterField(
            model_name='course',
            name='icon',
            field=models.URLField(help_text='URL of the course icon', max_length=300),
        ),
        migrations.AlterField(
            model_name='section',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='src.course'),
        ),
        migrations.AlterField(
            model_name='section',
            name='icon',
            field=models.URLField(help_text='URL of the section icon', max_length=1000),
        ),
        migrations.AlterField(
            model_name='tutorial',
            name='img',
            field=models.URLField(help_text='URL of the tutorial image', max_length=300),
        ),
    ]
