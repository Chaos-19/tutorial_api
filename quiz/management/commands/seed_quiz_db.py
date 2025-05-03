import json
from os import path
from django.core.management.base import BaseCommand
from src.models import Tutorial
from quiz.models import Quiz, Question, Option
import cloudinary.uploader

class Command(BaseCommand):
    help = 'Seeds the database with initial quiz data.'

    def handle(self, *args, **kwargs):
        base_dir = "example/assets-Angular"
        tutorial = Tutorial.objects.filter(title="Angular").first()
        if not tutorial:
            self.stdout.write(self.style.ERROR("Tutorial 'Angular' not found."))
            return

        quiz_data = [
            {"id": 723, "count": 20, "description": "assets/icons/leaf.svg", "quiz_icon": "assets/icons/html-1.svg", "name": "HTML", "slug": "html"},
            {"id": 7223, "count": 20, "description": "assets/icons/leaf.svg", "quiz_icon": "assets/icons/css-1.svg", "name": "CSS", "slug": "css"},
            {"id": 7123, "count": 35, "description": "assets/icons/leaf.svg", "quiz_icon": "assets/icons/javascript-2.svg", "name": "JavaScript", "slug": "javascript"},
            {"id": 7123, "count": 35, "description": "assets/icons/leaf.svg", "quiz_icon": "assets/icons/angular-6.svg", "name": "Angular", "slug": "angular"},
            {"id": 7123, "count": 35, "description": "assets/icons/leaf.svg", "quiz_icon": "assets/icons/ionic-1.svg", "name": "Ionic", "slug": "ionic"},
            {"id": 7123, "count": 35, "description": "assets/icons/leaf.svg", "quiz_icon": "assets/icons/nativescript-1.svg", "name": "NativeScript", "slug": "nativescript"},
            {"id": 7123, "count": 35, "description": "assets/icons/leaf.svg", "quiz_icon": "assets/icons/electron.svg", "name": "Electron", "slug": "electron"},
            {"id": 7123, "count": 35, "description": "assets/icons/leaf.svg", "quiz_icon": "assets/icons/d3.svg", "name": "D3", "slug": "d3"},
            {"id": 7123, "count": 35, "description": "assets/icons/leaf.svg", "quiz_icon": "assets/icons/graphql-1.svg", "name": "GraphQL", "slug": "graphql"}
        ]

        for data in quiz_data:
            icon_path = data['quiz_icon'].replace("assets", base_dir)
            try:
                result = cloudinary.uploader.upload(icon_path)
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Failed to upload icon {icon_path}: {e}"))
                continue

            quiz = Quiz(
                title=f"{data['name']} Basics",
                slug=f"{data['slug']}_{tutorial.title}",
                icon=result['public_id'],
                tutorial=tutorial
            )
            quiz.save()

            quiz_file = f"{base_dir}/quiz/angular/{data['slug']}.json"
            if path.exists(quiz_file):
                with open(quiz_file, "r") as f:
                    quizzes = json.load(f)

                for quiz_data in quizzes:
                    question = Question(
                        text=quiz_data['title'],
                        detail=quiz_data.get('detail', ''),
                        output=quiz_data.get('output', ''),
                        quiz=quiz
                    )
                    question.save()

                    for key, text in quiz_data['options'].items():
                        Option.objects.create(
                            question=question,
                            key=key,
                            text=text,
                            is_correct=(key.upper() == quiz_data['correct'].upper())
                        )
            else:
                self.stdout.write(self.style.WARNING(f"Quiz file {quiz_file} not found."))

        self.stdout.write(self.style.SUCCESS("Quiz database seeded successfully."))