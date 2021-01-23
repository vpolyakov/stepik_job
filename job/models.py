from django.db import models
from tinymce import HTMLField


# Create your models here.
class Company(models.Model):
    com_id = models.PositiveIntegerField(primary_key=True, db_column='id')
    name = models.CharField(max_length=32)
    location = models.CharField(max_length=32)
    logo = models.URLField(default='https://place-hold.it/100x60')
    description = models.CharField(max_length=264)
    employee_count = models.PositiveIntegerField()

    def __str__(self):
        return '%s' % self.name


class Specialty(models.Model):
    code = models.CharField(primary_key=True, max_length=20)
    title = models.CharField(max_length=40)
    picture = models.URLField(default='https://place-hold.it/100x60')

    def __str__(self):
        return '%s' % self.title


class Vacancy(models.Model):
    vacancy_id = models.PositiveIntegerField(primary_key=True, db_column='id')
    title = models.CharField(max_length=64)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='vacancies')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vacancies')
    skills = models.CharField(max_length=128)
    description = HTMLField('Description')
    salary_min = models.PositiveIntegerField()
    salary_max = models.PositiveIntegerField()
    published_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return '%s' % self.title
