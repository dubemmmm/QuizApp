from django.contrib import admin
from .models import Question, Option,  Quiz
# Register your models here.
class OptionInline(admin.TabularInline):
    model = Option

class QuestionInline(admin.TabularInline):
    model = Question
    inlines = [OptionInline]

admin.site.register(Quiz, inlines=[QuestionInline])
admin.site.register(Question, inlines=[OptionInline])
admin.site.register(Option)
