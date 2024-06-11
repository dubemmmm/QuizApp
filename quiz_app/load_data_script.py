import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_app.settings')
import django
django.setup()

import json
from app.models import Quiz, Question, Option

def load_json_data(json_filename):
    with open(json_filename, 'r') as file:
        data = json.load(file)

    quizzes_data = data.get('quizzes', [])
    for quiz_data in quizzes_data:
        quiz = Quiz.objects.create(title=quiz_data['title'], icon=quiz_data['icon'])

        questions_data = quiz_data.get('questions', [])
        for question_data in questions_data:
            question = Question.objects.create(quiz=quiz, questions_text=question_data['question'])
            
            options_data = question_data.get('options', [])
            for option_text in options_data:
                option = Option.objects.create(question=question, options_text=option_text)
                if option_text == question_data['answer']:
                    question.answer = option
                    question.save()

if __name__ == "__main__":
    json_filename = "quiz_data.json"
    load_json_data(json_filename)

