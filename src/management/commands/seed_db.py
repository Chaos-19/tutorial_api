# src/management/commands/seed_db.py
import json
from os import path
from django.core.management.base import BaseCommand
from src.models import Tutorial, Category, Course, Section, Lesson
from django.contrib.contenttypes.models import ContentType

import cloudinary.uploader

from src.gemini_test import generate
from django.db import transaction

class Command(BaseCommand):
    help = 'Seeds the database with initial data.'

    def handle(self, *args, **kwargs):
        base_dir = "example/assets-Angular"
        result = cloudinary.uploader.upload(f"{base_dir}/logo.png")
        tutorial = Tutorial(img=result['public_id'], title="Angular M")
        tutorial.save()

        files = [
          {
            'file': "categories/basic.json",
            'icon': "assets/main-icons/adv-web-dev.svg",
            'category': 'Learn the basic of web  development first',
            },
          {
            'file': "categories/angular.json",
            'icon': "assets/main-icons/angular-6.svg",
            'category': 'Learn Angular development',
            'bannerIcon': "assets/angular-poster.svg",
        
            },
          {
            'file': "categories/good_to_know.json",
            'icon': "assets/reading.png",
            'category': 'good to know',
        
            },
          {
            'file': "categories/web.json",
            'icon': "assets/main-icons/state.svg",
            'category': "Angular state management",
        
            },
          {
            'file': "categories/programming_lang.json",
            'icon': "assets/main-icons/mobile.svg",
            'category': "mobile app development with \n angular",
        
            },
          {
            'file': "categories/more_programming_lang.json",
            'icon': "assets/main-icons/pie-chart.png",
            'category': "working with chart",
        
            },
          {
            'file': "categories/advanced_web_development.json",
            'icon': "assets/main-icons/library.svg",
            'category': "must learn thrid party libraries",
        
            },
          {
            'file': "categories/machine.json",
            'icon': "assets/main-icons/computer.svg",
            'category': "development desktop apps with angular\n in electron",
        
            },
          {
            'file': "categories/apps_dev.json",
            'icon': "assets/main-icons/debugging.svg",
            'category': "testing angular application",
        
            },
          {
            'file': "categories/python_third_party.json",
            'icon': "assets/main-icons/utility.svg",
            'category': "utility libraries",
        
            },
          {
            'file': "categories/blockchain.json",
            'icon': "assets/main-icons/server-data-repository.svg",
            'category': "angular server side rendering"
            },
          {
            'file': "categories/datascience.json",
            'icon': "assets/main-icons/read.svg",
            'category': "angular best practice",
        
            },
          {
            'file': "categories/gui.json",
            'icon': "assets/main-icons/toolbox.svg",
            'category': "angular tools",
        
            }]
            
        for data in files:
            result = cloudinary.uploader.upload(data['icon'].replace("assets", base_dir))
            category_db = Category(name=data['category'], icon=result['public_id'], slug=data['category'].lower().replace(" ", "_"), tutorial=tutorial)
            category_db.save()
            with open(f"{base_dir}/{data['file']}", "r") as f:
                json_content = f.read()
                for item in json.loads(json_content):
                    result = cloudinary.uploader.upload(item['icon'].replace("assets", base_dir))
                    course_db = Course(
                        title=item['name'],
                        icon=result['public_id'],
                        description=item.get('courseInfo', item['description']),
                        is_nested=item['isNested'],
                        category=category_db
                    )
                    course_db.save()

                    if item['isNested']:
                        with open(f"{base_dir}/nested_categories/{item['postID']}.json", "r") as f:
                            sections = json.loads(f.read())
                            count = 1
                            for section in sections:
                                section_db = Section(
                                    title=section['name'],
                                    icon=course_db.icon,
                                    slug=section.get('slug',section['name'].lower().replace(" ", "_")),
                                    description=section.get('courseInfo', section['description']),
                                    course=course_db
                                )
                                section_db.save()
                                if path.exists(f"{base_dir}/nested_posts/{item['postID']}/{count}.json"):
                                    with open(f"{base_dir}/nested_posts/{item['postID']}/{count}.json", "r") as f:
                                        lessons = json.loads(f.read())
                                        for lesson in lessons:
                                            lesson_db = Lesson(
                                                title=lesson['title']['rendered'],
                                                content=lesson['content']['rendered'],
                                                content_type=ContentType.objects.get_for_model(section_db),
                                                object_id=section_db.id
                                            )
                                            lesson_db.save()
                                    count += 1
                    else:
                        with open(f"{base_dir}/posts/{item['postID']}.json", "r") as f:
                            lessons = json.loads(f.read())
                            for lesson in lessons:
                                lesson_db = Lesson(
                                    title=lesson['title']['rendered'],
                                    content=lesson['content']['rendered'],
                                    content_type=ContentType.objects.get_for_model(course_db),
                                    object_id=course_db.id
                                )
                                lesson_db.save()
        self.stdout.write(self.style.SUCCESS("Database seeded successfully."))
        
"""
# src/management/commands/seed_db.py
import json
import time
from os import path
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
import cloudinary.uploader
from src.models import Tutorial, Category, Course, Section, Lesson
from src.gemini_test import generate

class Command(BaseCommand):
    help = 'Seeds the database with initial data.'
    
    def handle(self, *args, **kwargs):
        base_dir = "example/assets-Angular"
        
        # Create tutorial
        tutorial = self.create_tutorial(base_dir)
        
        # Process all categories
        files = [
          {
            'file': "categories/basic.json",
            'icon': "assets/main-icons/adv-web-dev.svg",
            'category': 'Learn the basic of web  development first',
            },
          {
            'file': "categories/angular.json",
            'icon': "assets/main-icons/angular-6.svg",
            'category': 'Learn Angular development',
            'bannerIcon': "assets/angular-poster.svg",
        
            },
          {
            'file': "categories/good_to_know.json",
            'icon': "assets/reading.png",
            'category': 'good to know',
        
            },
          {
            'file': "categories/web.json",
            'icon': "assets/main-icons/state.svg",
            'category': "Angular state management",
        
            },
          {
            'file': "categories/programming_lang.json",
            'icon': "assets/main-icons/mobile.svg",
            'category': "mobile app development with \n angular",
        
            },
          {
            'file': "categories/more_programming_lang.json",
            'icon': "assets/main-icons/pie-chart.png",
            'category': "working with chart",
        
            },
          {
            'file': "categories/advanced_web_development.json",
            'icon': "assets/main-icons/library.svg",
            'category': "must learn thrid party libraries",
        
            },
          {
            'file': "categories/machine.json",
            'icon': "assets/main-icons/computer.svg",
            'category': "development desktop apps with angular\n in electron",
        
            },
          {
            'file': "categories/apps_dev.json",
            'icon': "assets/main-icons/debugging.svg",
            'category': "testing angular application",
        
            },
          {
            'file': "categories/python_third_party.json",
            'icon': "assets/main-icons/utility.svg",
            'category': "utility libraries",
        
            },
          {
            'file': "categories/blockchain.json",
            'icon': "assets/main-icons/server-data-repository.svg",
            'category': "angular server side rendering"
            },
          {
            'file': "categories/datascience.json",
            'icon': "assets/main-icons/read.svg",
            'category': "angular best practice",
        
            },
          {
            'file': "categories/gui.json",
            'icon': "assets/main-icons/toolbox.svg",
            'category': "angular tools",
        
            }]  # Your existing files array
        total_lessons = self.count_total_lessons(base_dir, files)
        processed = 0
        
        for data in files:
            category = self.create_category(base_dir, data, tutorial)
            self.process_category(base_dir, data, category, total_lessons, processed)
        
        self.stdout.write(self.style.SUCCESS("Database seeded successfully."))
    
    def create_tutorial(self, base_dir):
        result = cloudinary.uploader.upload(f"{base_dir}/logo.png")
        return Tutorial.objects.create(
            img=result['public_id'],
            title="Angular M"
        )
    
    def create_category(self, base_dir, data, tutorial):
        icon_path = data['icon'].replace("assets", base_dir)
        result = cloudinary.uploader.upload(icon_path)
        return Category.objects.create(
            name=data['category'],
            icon=result['public_id'],
            slug=data['category'].lower().replace(" ", "_"),
            tutorial=tutorial
        )
    
    def count_total_lessons(self, base_dir, files):
        total = 0
        for data in files:
            with open(f"{base_dir}/{data['file']}", "r") as f:
                items = json.loads(f.read())
                for item in items:
                    if item['isNested']:
                        total += self.count_nested_lessons(base_dir, item)
                    else:
                        total += self.count_flat_lessons(base_dir, item)
        return total
    
    def count_nested_lessons(self, base_dir, item):
        count = 0
        with open(f"{base_dir}/nested_categories/{item['postID']}.json", "r") as f:
            sections = json.loads(f.read())
            for i in range(len(sections)):
                lesson_file = f"{base_dir}/nested_posts/{item['postID']}/{i+1}.json"
                if path.exists(lesson_file):
                    with open(lesson_file, "r") as lf:
                        count += len(json.loads(lf.read()))
        return count
    
    def count_flat_lessons(self, base_dir, item):
        with open(f"{base_dir}/posts/{item['postID']}.json", "r") as f:
            return len(json.loads(f.read()))
    
    def process_category(self, base_dir, data, category, total_lessons, processed):
        with open(f"{base_dir}/{data['file']}", "r") as f:
            items = json.loads(f.read())
            for item in items:
                course = self.create_course(base_dir, item, category)
                if item['isNested']:
                    processed = self.process_nested_course(base_dir, item, course, total_lessons, processed)
                else:
                    processed = self.process_flat_course(base_dir, item, course, total_lessons, processed)
    
    def create_course(self, base_dir, item, category):
        icon_path = item['icon'].replace("assets", base_dir)
        result = cloudinary.uploader.upload(icon_path)
        return Course.objects.create(
            title=item['name'],
            icon=result['public_id'],
            description=item.get('courseInfo', item['description']),
            is_nested=item['isNested'],
            category=category
        )
    
    def process_nested_course(self, base_dir, item, course, total_lessons, processed):
        with open(f"{base_dir}/nested_categories/{item['postID']}.json", "r") as f:
            sections = json.loads(f.read())
            for i, section in enumerate(sections):
                section_obj = Section.objects.create(
                    title=section['name'],
                    icon=course.icon,
                    slug=section.get('slug', section['name'].lower().replace(" ", "_")),
                    description=section.get('courseInfo', section['description']),
                    course=course
                )
                processed = self.process_lessons(
                    base_dir=base_dir,
                    post_id=item['postID'],
                    count=i+1,
                    parent=section_obj,
                    total_lessons=total_lessons,
                    processed=processed
                )
        return processed
    
    def process_flat_course(self, base_dir, item, course, total_lessons, processed):
        return self.process_lessons(
            base_dir=base_dir,
            post_id=item['postID'],
            count=None,
            parent=course,
            total_lessons=total_lessons,
            processed=processed
        )
    
    def process_lessons(self, base_dir, post_id, count, parent, total_lessons, processed):
        lesson_file = (
            f"{base_dir}/nested_posts/{post_id}/{count}.json" 
            if count else 
            f"{base_dir}/posts/{post_id}.json"
        )
        
        if not path.exists(lesson_file):
            return processed
            
        with open(lesson_file, "r") as f:
            lessons = json.loads(f.read())
            for lesson in lessons:
                self.process_single_lesson(lesson, parent, total_lessons, processed)
                processed += 1
                self.print_progress(processed, total_lessons)
        return processed
    
    def process_single_lesson(self, lesson, parent, total_lessons, processed_count):
        while True:
            try:
                with transaction.atomic():
                    content = generate(lesson['content']['rendered'])
                    if not content.strip():
                        raise ValueError("Empty content generated")
                    
                    Lesson.objects.update_or_create(
                        title=lesson['title']['rendered'],
                        defaults={
                            'content': content,
                            'content_type': ContentType.objects.get_for_model(parent),
                            'object_id': parent.id
                        }
                    )
                    return
            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f"Error processing lesson '{lesson['title']['rendered']}': {str(e)}. Retrying..."
                ))
                time.sleep(5)
    
    def print_progress(self, processed, total):
        progress = processed / total * 100
        self.stdout.write(
            f"\rProcessing: {processed}/{total} ({progress:.1f}%)",
            ending='\r' if processed < total else '\n'
        )
        self.stdout.flush()

"""