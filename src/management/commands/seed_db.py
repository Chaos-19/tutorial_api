# src/management/commands/seed_db.py
import json
from os import path
from django.core.management.base import BaseCommand
from src.models import Tutorial, Category, Course, Section, Lesson
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Seeds the database with initial data.'

    def handle(self, *args, **kwargs):
        tutorial = Tutorial(img="http://test/img-url.png", title="Angular")
        tutorial.save()

        base_dir = "example/assets-Angular"
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
        
            }];
        for data in files:
            category_db = Category(name=data['category'], icon=data['icon'], slug=data['category'].lower().replace(" ", "_"), tutorial=tutorial)
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