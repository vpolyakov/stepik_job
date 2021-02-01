from django import forms
from django.contrib.auth.models import User
from django.forms import Textarea
from django.forms.widgets import FileInput
from django.utils.translation import gettext_lazy as _

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
        }
