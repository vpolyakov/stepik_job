from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView, TemplateView, CreateView, UpdateView

from job.forms import MyVacancyForm
from job.models import Vacancy, Company, Application


@method_decorator(login_required, name='dispatch')
class MyCompVacanciesView(ListView):
    model = Vacancy
    template_name = 'job/my_vacancy-list.html'
    context_object_name = 'vacancies'

    def get_queryset(self):
        if not Company.objects.filter(owner=self.request.user):
            redirect('/')  # TODO Не работает редирект
            return
        company = Company.objects.get(owner=self.request.user)
        vacancies = self.model.objects.filter(company=company)
        if not vacancies:
            return redirect('/mycompany/vacancies/letsstart/')
        return vacancies.annotate(application_count=Count('applications'))


@method_decorator(login_required, name='dispatch')
class MyCompVacancyLetsStartView(TemplateView):
    template_name = 'job/my-vacancy-start.html'


@method_decorator(login_required, name='dispatch')
class MyCompVacancyCreateView(LoginRequiredMixin, CreateView):
    form_class = MyVacancyForm
    template_name = 'job/my_vacancy-edit.html'
    success_url = '/mycompany/vacancies/'


@method_decorator(login_required, name='dispatch')
class MyCompVacancyUpdateView(UpdateView):
    form_class = MyVacancyForm
    model = Vacancy
    template_name = 'job/my_vacancy-edit.html'
    success_url = '/mycompany/vacancies/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['applications'] = Application.objects.filter(vacancy=self.object)
        context['pk'] = self.kwargs['pk']

        return context
