import json
import logging
from os import path
from django.core.management.base import BaseCommand
from django.db import transaction, IntegrityError
from src.models import Tutorial
from interview_question.models import Interview, Question
from django.contrib.contenttypes.models import ContentType
import cloudinary.uploader
from src.utils import format_md, html_to_markdown

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(),  # Console output
        logging.FileHandler('seed_interviews.log'),  # Log to file
    ]
)

class Command(BaseCommand):
    help = 'Seeds the database with initial Angular interview data.'

    def handle(self, *args, **kwargs):
        base_dir = "example/assets-Angular"
        logger.info(f"Starting database seeding from {base_dir}")

        # Check if Tutorial exists
        tutorial = Tutorial.objects.filter(title="Angular").first()
        if not tutorial:
            logger.error("No Tutorial found with title 'Angular'")
            self.stdout.write(self.style.ERROR("No Tutorial found with title 'Angular'"))
            return

        # Upload tutorial logo
        logo_path = f"{base_dir}/logo.png"
        if not path.exists(logo_path):
            logger.error(f"Logo file not found: {logo_path}")
            self.stdout.write(self.style.ERROR(f"Logo file not found: {logo_path}"))
            return
        '''
        try:
            logger.info(f"Uploading logo: {logo_path}")
            result = cloudinary.uploader.upload(logo_path)
            logger.info(f"Logo uploaded successfully: {result.get('public_id')}")
        except Exception as e:
            logger.error(f"Failed to upload logo: {str(e)}")
            self.stdout.write(self.style.ERROR(f"Failed to upload logo: {str(e)}"))
            return
        '''
        # Process interviews
        interviews_file = f"{base_dir}/interviews/angular/angular_home.json"
        if not path.exists(interviews_file):
            logger.error(f"Interviews file not found: {interviews_file}")
            self.stdout.write(self.style.ERROR(f"Interviews file not found: {interviews_file}"))
            return

        try:
            with open(interviews_file, "r") as f:
                interviews = json.load(f)
                logger.info(f"Loaded {len(interviews)} interviews from {interviews_file}")
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Failed to read or parse {interviews_file}: {str(e)}")
            self.stdout.write(self.style.ERROR(f"Failed to read or parse {interviews_file}: {str(e)}"))
            return

        for index, item in enumerate(interviews, 1):
            self.process_interview(item, tutorial, base_dir, index)

        logger.info("Database seeding completed successfully")
        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully"))

    def process_interview(self, item, tutorial, base_dir, index):
        logger.info(f"Processing interview {index}: {item.get('name', 'Unnamed')}")

        # Validate required fields
        required_fields = ['name', 'icon', 'postID']
        missing_fields = [field for field in required_fields if not item.get(field)]
        if missing_fields:
            logger.error(f"Interview {index} missing required fields: {missing_fields}")
            self.stdout.write(self.style.ERROR(f"Interview {index} missing required fields: {missing_fields}"))
            return

        # Upload icon
        icon_path = item['icon'].replace("assets", base_dir)
        if not path.exists(icon_path):
            logger.error(f"Icon file not found for interview {index}: {icon_path}")
            self.stdout.write(self.style.ERROR(f"Icon file not found: {icon_path}"))
            return

        try:
            logger.info(f"Uploading icon for interview {index}: {icon_path}")
            result = cloudinary.uploader.upload(icon_path)
            icon_public_id = result.get('public_id')
            if not icon_public_id:
                raise ValueError("No public_id in Cloudinary response")
            logger.info(f"Icon uploaded successfully: {icon_public_id}")
        except Exception as e:
            logger.error(f"Failed to upload icon for interview {index}: {str(e)}")
            self.stdout.write(self.style.ERROR(f"Failed to upload icon for interview {index}: {str(e)}"))
            return

        # Create Interview
        slug = f"{item['name'].lower().replace(' ', '-')}_{tutorial.title.lower()}"
        try:
            with transaction.atomic():
                interview = Interview(
                    title=item['name'],
                    slug=slug,
                    icon=icon_public_id,
                    tutorial=tutorial
                )
                interview.save()
                logger.info(f"Created interview {index}: {interview.title} (slug: {slug})")
        except IntegrityError as e:
            logger.error(f"Failed to save interview {index} due to duplicate slug or other integrity error: {str(e)}")
            self.stdout.write(self.style.ERROR(f"Failed to save interview {index}: {str(e)}"))
            return
        except Exception as e:
            logger.error(f"Failed to save interview {index}: {str(e)}")
            self.stdout.write(self.style.ERROR(f"Failed to save interview {index}: {str(e)}"))
            return

        # Process questions
        questions_file = f"{base_dir}/interviews/angular/{item['postID']}.json"
        if not path.exists(questions_file):
            logger.error(f"Questions file not found for interview {index}: {questions_file}")
            self.stdout.write(self.style.ERROR(f"Questions file not found: {questions_file}"))
            return

        try:
            with open(questions_file, "r") as f:
                questions = json.load(f)
                logger.info(f"Loaded {len(questions)} questions for interview {index}")
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Failed to read or parse {questions_file}: {str(e)}")
            self.stdout.write(self.style.ERROR(f"Failed to read or parse {questions_file}: {str(e)}"))
            return

        for q_index, question in enumerate(questions, 1):
            self.process_question(question, interview, index, q_index)

    def process_question(self, question, interview, interview_index, q_index):
        logger.info(f"Processing question {q_index} for interview {interview_index}")

        # Validate required fields
        if not question.get('title', {}).get('rendered') or not question.get('content', {}).get('rendered'):
            logger.error(f"Question {q_index} in interview {interview_index} missing title or content")
            self.stdout.write(self.style.ERROR(f"Question {q_index} missing title or content"))
            return

        try:
            with transaction.atomic():
                interview_question = Question(
                    interview=interview,
                    interview_question=question['title']['rendered'],
                    answer=html_to_markdown(format_md(question['content']['rendered']))
                )
                interview_question.save()
                logger.info(f"Created question {q_index} for interview {interview_index}: {interview_question.interview_question[:50]}")
        except Exception as e:
            logger.error(f"Failed to save question {q_index} for interview {interview_index}: {str(e)}")
            self.stdout.write(self.style.ERROR(f"Failed to save question {q_index}: {str(e)}"))
            
'''
import json
from os import path
from django.core.management.base import BaseCommand
from src.models import Tutorial, Category, Course, Section, Lesson
from django.contrib.contenttypes.models import ContentType

import cloudinary.uploader

from src.gemini_test import generate
from django.db import transaction

from src.utils import format_md,html_to_markdown

class Command(BaseCommand):
    help = 'Seeds the database with initial data.'

    def handle(self, *args, **kwargs):
        base_dir = "example/assets-Angular"
        result = cloudinary.uploader.upload(f"{base_dir}/logo.png")
        tutorial = Tutorial.objects.filter(title="Angular").first()
        
        with open(f"{base_dir}/interviews/angular/angular_home.json", "r") as f:
            interviews = json.loads(f.read())
            
            for item in interviews:
                result = cloudinary.uploader.upload(item['icon'].replace("assets", base_dir))
                interview = Interview(title=item.get('name'),slug=f"{item.get('name')}_{tutorial.title}", icon=result['public_id'],tutorial=tutorial)
                interview.save()
                with open(f"{base_dir}/interviews/angular/{item['postID']}.json", "r") as f:
                    interview_questions = json.loads(f.read())
                    
                    for question in interview_questions:
                        interview_question = Question(interview=interview,interview_question=question['title']['rendered'],answer=html_to_markdown(format_md(question['content']['rendered'])))
                        
                        interview_question.save()                            
 '''               
                

