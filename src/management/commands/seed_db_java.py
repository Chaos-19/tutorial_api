from src.models import Tutorial, Category, Course, Section, Lesson
from src.serializers import TutorialSerializer
from django.contrib.contenttypes.models import ContentType
import cloudinary.uploader
import json
from os import path
from src.gemini_test import generate
from src.utils import format_md, html_to_markdown

tutorial = "course Test"
base_dir = "example/assets-Java"

# Upload tutorial image and create Tutorial
result = cloudinary.uploader.upload(f"{base_dir}/java_free.png",public_id=etag,overwrite=False)
tutorial = Tutorial(img=result['public_id'], title="Java")
tutorial.save()

files = [
    {'category': 'Basics', 'file': 'categories/basic.json', 'icon': "main-icons/basics-2.svg"},
    {'category': 'Learn Java', 'file': 'categories/pythonVs.json', 'icon': "main-icons/java-6.svg"},
    {'category': 'Intermediate Concepts', 'file': 'categories/datascience.json', 'icon': "main-icons/java-5.svg"},
    {'category': 'Java Libraries', 'file': 'categories/web.json', 'icon': "main-icons/java-7.svg"},
    {'category': 'Advanced Concepts', 'file': 'categories/more_programming_lang.json', 'icon': "main-icons/java-6.svg"},
    {'category': 'GUI Development', 'file': 'categories/advanced_web_development.json', 'icon': "main-icons/gui.svg"},
    {'category': 'Web Development', 'file': 'categories/programming_lang.json', 'icon': "main-icons/website-layout.svg"},
    {'category': 'Third Party', 'file': 'categories/apps_dev.json', 'icon': "main-icons/toolbox.svg"},
    {'category': 'Testing', 'file': 'categories/gui.json', 'icon': "main-icons/toolbox.svg"},
    {'category': 'Database', 'file': 'categories/database.json', 'icon': "main-icons/database.svg"},
]

try:
    for data in files:
        # Upload category icon
        result = cloudinary.uploader.upload(f"{base_dir}/{data['icon']}",public_id=etag,overwrite=False)

        # Modify category slug to include tutorial name
        category_slug = f"{tutorial.title.lower()}_{data['category'].lower().replace(' ', '_')}"
        category_db = Category(
            name=data['category'],
            icon=result['public_id'],
            slug=category_slug,
            tutorial=tutorial
        )
        category_db.save()

        # Read JSON file for courses
        with open(f"{base_dir}/{data['file']}", "r") as f:
            json_content = f.read()

            for item in json.loads(json_content):
                # Upload course icon
                result = cloudinary.uploader.upload(item['icon'].replace("assets", base_dir),public_id=etag,overwrite=False)

                # Course creation (no slug field in original code)
                course_db = Course(
                    title=item['name'],
                    icon=result['public_id'],
                    description=item['courseInfo'] if 'courseInfo' in item else item['description'],
                    category=category_db
                )
                course_db.save()

                if item['isNested']:
                    # Handle nested sections
                    with open(f"{base_dir}/nested_categories/{item['postID']}.json", "r") as f:
                        json_file = f.read()
                        sections = json.loads(json_file)
                    count = 1
                    for section in sections:
                        # Modify section slug to include tutorial name
                        section_slug = f"{tutorial.title.lower()}_{section['name'].lower().replace(' ', '_')}_{section['slug']}"
                        section_db = Section(
                            title=section['name'],
                            icon=course_db.icon,
                            slug=section_slug,
                            description=section['description'] if 'description' in section else section['courseInfo'],
                            course=course_db
                        )
                        section_db.save()

                        # Handle lessons for the section
                        if path.exists(f"{base_dir}/nested_posts/{item['postID']}/{count}.json"):
                            with open(f"{base_dir}/nested_posts/{item['postID']}/{count}.json", "r") as f:
                                json_file = f.read()
                                lessons = json.loads(json_file)

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
                    # Handle lessons directly under course
                    with open(f"{base_dir}/posts/{item['postID']}.json", "r") as f:
                        json_file = f.read()
                        lessons = json.loads(json_file)

                    for lesson in lessons:
                        lesson_db = Lesson(
                            title=lesson['title']['rendered'],
                            content=html_to_markdown(format_md(lesson['content']['rendered'])),
                            object_id=course_db.id,
                            content_type=ContentType.objects.get_for_model(course_db)
                        )
                        lesson_db.save()
except Exception as e:
    print(e)
    raise e
 