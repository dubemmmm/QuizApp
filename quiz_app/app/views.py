from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Quiz, Question, Option
from django.http import HttpResponse, JsonResponse
from app.utils import question_count
from django.views.generic import View
from django.shortcuts import redirect

# Create your views here.    
def home(request):
    request.session['question_count'] = 0
    request.session['score'] = 0
    return render(request, 'app/homepage.html')

class NextQuestionView(View):
    template_name = 'app/questions.html'

    def get_current_question(self, quiz, question_count):
        questions = quiz.questions.all()
        print('the count when nextquestionview is called ', question_count)
        if question_count < len(questions):
            return questions[question_count]
        #print('current question ', questions[question_count])
        return None

    def get(self, request, quiz_id):
        print('the quiz_id', quiz_id)
        question_count = request.session.get('question_count', 0)
        score = request.session.get('score', 0)
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        print(quiz.title)
        current_question = self.get_current_question(quiz, question_count)
        if current_question:
            
            context = {'quiz': quiz, 'current_question': current_question, 'question_count': question_count, 'score': score}
            print('the quiz id is ', quiz_id)
            return render(request, self.template_name, context)
        else:
            # No more questions, render the score
            context = {'quiz': quiz, 'score': score}
            return render(request, 'app/score.html', context)



class CheckAnswerView(View):
    def get_current_question(self, quiz, question_count):
        questions = quiz.questions.all()
        if question_count < len(questions):
            current_question = questions[question_count]
            return current_question
        return None
    
    def check_answer(self, current_question, selected_option_id):
        if current_question is None or selected_option_id is None:
            return False
        selected_option = get_object_or_404(Option, pk=selected_option_id)
        correct_answer = current_question.answer
        if selected_option is not None and correct_answer is not None:
            is_correct = selected_option == correct_answer
        else:
            is_correct = False
        return is_correct
        
    def post(self, request, quiz_id):
        print('quiz_id is: ', quiz_id)
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        print('quiz iz: ', quiz)
        question_count = request.session.get('question_count', 0)
        score = request.session.get('score', 0)
        current_question = self.get_current_question(quiz, question_count)
        selected_option_id = request.POST.get('selected_option_id')
        
        is_correct = self.check_answer(current_question, selected_option_id)
        selected_option = get_object_or_404(Option, pk=selected_option_id)
        correct_answer = current_question.answer
        print('the count is', question_count)
        print('the current question is: ', current_question)
        print('the selected option is: ', selected_option)
        print('the correct answer is: ', correct_answer)
        print('you got the question: ', is_correct)
        if is_correct:
            score += 1
            print(f"Correct! Current Score: {score}")
        question_count +=1
        request.session['question_count'] = question_count
        request.session['score'] = score
        
        return redirect('app:next_question', quiz_id=quiz_id)


