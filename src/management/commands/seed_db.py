# src/management/commands/seed_db.py
import json
from os import path
from django.core.management.base import BaseCommand
from src.models import Tutorial, Category, Course, Section, Lesson
from django.contrib.contenttypes.models import ContentType
import cloudinary.uploader
import cloudinary.api
from src.gemini_test import generate
from src.utils import format_md, html_to_markdown
from django.db import transaction
import hashlib

class Command(BaseCommand):
    help = 'Seeds the database with initial data.'

    def get_cloudinary_public_id(self, file_path):
        """Generate a public_id based on the file path."""
        return hashlib.md5(file_path.encode()).hexdigest()

    def check_and_upload_image(self, file_path, public_id):
        """Check if image exists in Cloudinary; upload if it doesn't."""
        try:
            # Check if the resource exists in Cloudinary
            cloudinary.api.resource(public_id)
            # If resource exists, return the public_id
            return public_id
        except cloudinary.exceptions.Error:
            # If resource doesn't exist, upload the image
            result = cloudinary.uploader.upload(
                file_path,
                public_id=public_id,
                overwrite=False
            )
            return result['public_id']

    def handle(self, *args, **kwargs):
        base_dir = "example/assets-Angular"

        # Upload tutorial logo
        logo_path = f"{base_dir}/logo.png"
        etag = self.get_cloudinary_public_id(logo_path)
        public_id = self.check_and_upload_image(logo_path, etag)
        tutorial = Tutorial(img=public_id, title="Angular")
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
            icon_path = data['icon'].replace("assets", base_dir)
            etag = self.get_cloudinary_public_id(icon_path)
            public_id = self.check_and_upload_image(icon_path, etag)
            category_db = Category(
                name=data['category'],
                icon=public_id,
                slug=data['category'].lower().replace(" ", "_"),
                tutorial=tutorial
            )
            category_db.save()

            with open(f"{base_dir}/{data['file']}", "r") as f:
                json_content = f.read()
                for item in json.loads(json_content):
                    icon_path = item['icon'].replace("assets", base_dir)
                    etag = self.get_cloudinary_public_id(icon_path)
                    public_id = self.check_and_upload_image(icon_path, etag)
                    course_db = Course(
                        title=item['name'],
                        icon=public_id,
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
                                    slug=section.get('slug', section['name'].lower().replace(" ", "_")),
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
                                                content=html_to_markdown(format_md(lesson['content']['rendered'])),
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
                                    content=html_to_markdown(format_md(lesson['content']['rendered'])),
                                    content_type=ContentType.objects.get_for_model(course_db),
                                    object_id=course_db.id
                                )
                                lesson_db.save()

        self.stdout.write(self.style.SUCCESS("Database seeded successfully."))
