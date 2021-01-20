import os
import django

os.environ["DJANGO_SETTINGS_MODULE"] = 'stepik_job.settings'
django.setup()

from data import specialties, companies, jobs
from job.models import Company, Specialty, Vacancy


def fill_specialties():
    for spec in specialties:
        Specialty.objects.create(
            code=spec['code'],
            title=spec['title'],
            picture=f"specialties/specty_{spec['code']}.png",
        )


def fill_companies():
    for company in companies:
        Company.objects.create(
            id=company['id'],
            name=company['title'],
            location=company['location'],
            logo=company['logo'],  # Возможно надо прописывать еще static/ в начале пути.
            description=company['description'],
            employee_count=company['employee_count'],
        )


def fill_vacancies():
    for job in jobs:
        Vacancy.objects.create(
            id=job['id'],
            title=job['title'],
            specialty=Specialty.objects.get(code=job['specialty']),
            company=Company.objects.get(id=int(job['company'])),
            skills=job['skills'],
            description=job['description'],
            salary_min=job['salary_from'],
            salary_max=job['salary_to'],
            published_at=job['posted'],
        )


def fill_data_base():
    fill_specialties()
    fill_companies()
    fill_vacancies()


if __name__ == '__main__':
    fill_data_base()
