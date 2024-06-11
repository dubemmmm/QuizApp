from django.db import models

# Create your models here.
class Quiz(models.Model):
    title = models.CharField(max_length=255)
    icon = models.ImageField(upload_to='quizzes/icons', blank=True)
    
    def __str__(self):
        return self.title
    
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    questions_text = models.CharField(max_length=255)
    answer = models.ForeignKey('Option', related_name='correct_for_question', on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.questions_text

class Option(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    options_text = models.CharField(max_length=500)
    
    def __str__(self):
        return self.options_text