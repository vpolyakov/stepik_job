from django.views.generic import ListView, DetailView

from job.models import Vacancy


class MycompanyVacanciesView(ListView):
    model = Vacancy
    template_name = 'job/my_vacancy-list.html'


class MycompanyVacancyView(DetailView):
    model = Vacancy
    template_name = 'job/my_vacancy-edit.html'
