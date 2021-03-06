from django.db.models import Count
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, ListView, TemplateView

# Create your views here.
from job.forms import ApplicationForm
from job.models import Vacancy, Specialty, Company


class MainView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['spec_vacancies_count'] = Specialty.objects.annotate(vacancy_count=Count('vacancies'))
        context['companies_vacancies_count'] = Company.objects.annotate(vacancy_count=Count('vacancies'))
        return context


class ListVacanciesView(ListView):
    model = Vacancy

    def get_queryset(self):
        return Vacancy.objects.select_related('specialty', 'company')

    context_object_name = 'vacancies'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vacancies_count'] = context['vacancies'].count()
        context['title'] = 'Вакансии'
        return context


class ListSpecVacanciesView(ListVacanciesView):

    def get_queryset(self):
        self.specialty = get_object_or_404(Specialty, code=self.kwargs['code'])
        return super().get_queryset().filter(specialty=self.specialty)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.specialty.title
        return context


class ListCompanyVacanciesView(ListView):

    template_name = 'job/company_vacancy_list.html'
    context_object_name = 'vacancies'

    def get_queryset(self):
        self.company = get_object_or_404(Company, com_id=self.kwargs['pk'])
        return (
            Vacancy.objects
            .select_related('specialty', 'company')
            .filter(company=self.company)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vacancies_count'] = context['vacancies'].count()
        context['company'] = self.company
        return context


class DetailVacancyView(DetailView):
    model = Vacancy
    queryset = Vacancy.objects.select_related('company')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ApplicationForm()
        return context


class VacancySendView(TemplateView):
    template_name = 'job/sent.html'

    def post(self, request, **kwargs):
        form = ApplicationForm(request.POST)
        if form.is_valid():
            form.vacancy_id = kwargs['vacancy_id']
            if request.user.is_authenticated:
                form.curr_user = request.user
            form.save()
            return redirect(request.path)


def custom_handler404(request, exception) -> HttpResponse:
    return HttpResponseNotFound('<h1>404<h1><h2>The requested resource was not found on the server.</h2>')


def custom_handler500(request) -> HttpResponse:
    return HttpResponseServerError('<h1>500</h1><h2>That happened internal server error.</h2>')
