from django import forms
from django.contrib.auth.models import User
from django.forms import Textarea
from django.forms.widgets import FileInput
from django.utils.translation import gettext_lazy as _
from tinymce.widgets import TinyMCE

from job.models import Application, Vacancy, Company


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('written_username', 'written_phone', 'written_cover_letter')
        labels = {
            'written_username': _('Вас зовут'),
            'written_phone': _('Ваш телефон'),
            'written_cover_letter': _('Сопроводительное письмо'),
        }
    vacancy_id = None
    curr_user = User.objects.get(id=0)

    def save(self, commit=True):
        application_letter = super().save(commit=False)
        application_letter.vacancy = Vacancy.objects.get(vacancy_id=self.vacancy_id)
        application_letter.user = self.curr_user
        if commit:
            application_letter.save()
        return application_letter


class MyCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name', 'location', 'logo', 'description', 'employee_count')
        labels = {
            'name': _('Название компании'),
            'location': 'География',
            'logo': '',
            'description': _('Информация о компании'),
            'employee_count': _('Количество человек в компании'),
        }
        widgets = {
            'description': Textarea(attrs={'rows': 4}),
            'logo': FileInput(attrs={'class': 'custom-file-input'}),
            # TODO Доработать (сделать пользовательский) виджет, чтобы из поля передавалось в html tag img<> адрес
        }


class MyVacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ('title', 'specialty', 'skills', 'description', 'salary_min', 'salary_max')
        labels = {
            'title': 'Название вакансии',
            'specialty': 'Специализация',
            'skills': 'Требуемые навыки',
            'description': 'Описание вакансии',
            'salary_min': 'Зарплата от',
            'salary_max': 'Зарплата до',
        }
        widgets = {
            'skills': Textarea(attrs={'rows': 2}),
            'description': TinyMCE(
                attrs={'cols': 80, 'rows': 14, 'maxwidth': 678},
                mce_attrs={'width': 678,
                           'menubar': False,
                           'toolbar2': "",
                           'toolbar1': '''
                           bold italic underline | fontselect,
                           fontsizeselect | forecolor backcolor | alignleft alignright aligncenter alignjustify |
                            bullist numlist | link image
                           ''',
                           'plugins': '''
                            textcolor save link image media contextmenu
                            lists insertdatetime nonbreaking
                            contextmenu directionality searchreplace wordcount visualblocks
                            visualchars code autolink lists charmap print hr
                            anchor pagebreak
                            ''',
                           },
            ),
        }
