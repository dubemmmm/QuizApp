from django.urls import path
from .views import home,  NextQuestionView, CheckAnswerView

app_name = 'app'
urlpatterns = [
    path('', home, name='home'),
    path('quiz/<int:quiz_id>/', NextQuestionView.as_view(), name='next_question'),
    path('check_answers/<int:quiz_id>/', CheckAnswerView.as_view(), name='check_answers'),

    
]
