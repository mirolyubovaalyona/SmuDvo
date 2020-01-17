from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Question, Answer

class IndexView(ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_questions_list'

    def get_queryset(self):
        """Вернуть 2 последних свежих опроса"""
        return Question.objects.order_by('-date_published')[:2]