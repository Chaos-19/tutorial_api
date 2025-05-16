from src.models import Tutorial,Category,Course,Section,Lesson
from src.serializers import TutorialSerializer

from django.contrib.contenttypes.models import ContentType
import cloudinary.uploader

import json
from os import path
from src.gemini_test import generate
from src.utils import format_md,html_to_markdown

tutorial = "course Test"
base_dir = "example/assets-Flutter"

result = cloudinary.uploader.upload(f"{base_dir}/logo.png",public_id=etag,overwrite=False)
tutorial = Tutorial(img=result['public_id'],title="Flutter")

tutorial.save()

files = [
   {'category':'Getting Started','file':'categories/basic.json','icon':"icons/flutter-4.svg"},
   {'category':'Dart basics' , 'file':'categories/web.json','icon':"icons/flutter-4.svg"},
  {'category':'Flutter Widgets' , 'file':'categories/programming_lang.json','icon':"icons/flutter-4.svg"}, 
  {'category':'Gestures & Inputs' , 'file':'categories/pythonVs.json','icon':"icons/flutter-4.svg"},
  {'category':'Flutter Animation' , 'file':'categories/machine_basics.json','icon':"icons/flutter-4.svg"},
  {'category':'Routing' , 'file':'categories/more_programming_lang.json','icon':"icons/flutter-4.svg"}, 
  {'category':'Working with Plugins' , 'file':'categories/basic_database.json','icon':"icons/flutter-4.svg"}, 
  {'category':'Testing & Debugging' , 'file':'categories/datascience.json','icon':"icons/flutter-4.svg"}, 
  {'category':'Releasing Your App' , 'file':'categories/advanced_web_development.json','icon':"icons/flutter-4.svg"}, 
  {'category':'Flutter Project' , 'file':'categories/blockchain.json','icon':"icons/coding-1.svg"}, 
  ]
try:
    for data in files:
        result = cloudinary.uploader.upload(f"{base_dir}/{data['icon']}",public_id=etag,overwrite=False)
        category = {'name': data['category'], 'icon': result['public_id'], 'slug': 'getting_started'}
        category_db = Category(name=data['category'], icon=result['public_id'], slug=data['category'].lower().replace(" ", "_"), tutorial=tutorial)
        category_db.save()
        with open(f"{base_dir}/{data['file']}", "r") as f:
            json_content = f.read()

            for item in json.loads(json_content):
                result = cloudinary.uploader.upload(item['icon'].replace("assets", base_dir),public_id=etag,overwrite=False)
                course = {'name': item['name'], 'icon': result['public_id'], 'description': item['postID']}
                course_db = Course(title=item['name'], icon=result['public_id'], description=item['courseInfo'] if 'courseInfo' in item else item['description'], category=category_db)
                course_db.save()
                if item['isNested']:
                    with open(f"{base_dir}/nested_categories/{item['postID']}.json", "r") as f:
                        json_file = f.read()
                        sections = json.loads(json_file)
                    count = 1
                    for section in sections:
                        section_data = {'name': section['name'], 'icon': course['icon'], 'description': section['description'] if 'description' in section else section['courseInfo'], 'slug': section['slug']}
                        # print(section_data)
                        section_db = Section(title=section['name'], icon=course['icon'], slug=section['slug'], description=section['description'] if 'description' in section else section['courseInfo'], course=course_db)
                        section_db.save()
                        if path.exists(f"{base_dir}/nested_posts/{item['postID']}/{count}.json"):
                            with open(f"{base_dir}/nested_posts/{item['postID']}/{count}.json", "r") as f:
                                json_file = f.read()

                                lessons = json.loads(json_file)

                                for lesson in lessons:
                                    # print(lesson['title']['rendered'])
                                    lesson_db = Lesson(title=lesson['title']['rendered'], content=html_to_markdown(format_md(lesson['content']['rendered'])), content_type=ContentType.objects.get_for_model(section_db), object_id=section_db.id)
                                    lesson_db.save()

                            count += 1
                else:
                    with open(f"{base_dir}/posts/{item['postID']}.json", "r") as f:
                        json_file = f.read()

                    lessons = json.loads(json_file)

                    for lesson in lessons:
                        # print(lesson['title']['rendered'])
                        lesson_db = Lesson(title=lesson['title']['rendered'], content=html_to_markdown(format_md(lesson['content']['rendered'])), object_id=course_db.id, content_type=ContentType.objects.get_for_model(course_db))
                        lesson_db.save()
except Exception as e:
    print(e)
    raise e