# src/management/commands/seed_db.py
import json
from os import path
from django.core.management.base import BaseCommand
from src.models import Tutorial, Category, Course, Section, Lesson
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Seeds the database with initial data.'

    def handle(self, *args, **kwargs):
        tutorial = Tutorial(img="http://test/img-url.png", title="Flutter")
        tutorial.save()

        base_dir = "example/assets-Flutter"
        files = [
            {'category': 'Getting Started', 'file': 'categories/basic.json'},
            {'category': 'Dart basics', 'file': 'categories/web.json'},
            {'category': 'Flutter Widgets', 'file': 'categories/programming_lang.json'},
            {'category': 'Gestures & Inputs', 'file': 'categories/pythonVs.json'},
            {'category': 'Flutter Animation', 'file': 'categories/machine_basics.json'},
            {'category': 'Routing', 'file': 'categories/more_programming_lang.json'},
            {'category': 'Working with Plugins', 'file': 'categories/basic_database.json'},
            {'category': 'Testing & Debugging', 'file': 'categories/datascience.json'},
            {'category': 'Releasing Your App', 'file': 'categories/advanced_web_development.json'},
            {'category': 'Flutter Project', 'file': 'categories/blockchain.json'},
        ]

        for data in files:
            category_db = Category(name=data['category'], icon=data['category'][:3].lower(), slug=data['category'].lower().replace(" ", "_"), tutorial=tutorial)
            category_db.save()
            with open(f"{base_dir}/{data['file']}", "r") as f:
                json_content = f.read()
                for item in json.loads(json_content):
                    course_db = Course(
                        title=item['name'],
                        icon=item['icon'],
                        description=item.get('courseInfo', item['description']),
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
                                    slug=section['slug'],
                                    description=section.get('description', section['courseInfo']),
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