from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, ListView

from assignments.models import Quiz


class AllQuizzesView(ListView):
    template_name = "assignments/quiz_list.html"
    model = Quiz
    queryset = model.objects.all()
