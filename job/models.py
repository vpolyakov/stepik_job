from django.contrib.auth.models import User
from django.db import models
from tinymce import HTMLField

from stepik_job.settings import MEDIA_COMPANY_IMAGE_DIR, MEDIA_SPECIALITY_IMAGE_DIR


# Create your models here.
class Company(models.Model):
    com_id = models.AutoField(primary_key=True, db_column='id')
    name = models.CharField(max_length=32)
    location = models.CharField(max_length=32)
    logo = models.ImageField(upload_to=MEDIA_COMPANY_IMAGE_DIR, default='150x80.gif')
    description = models.CharField(max_length=264)
    employee_count = models.PositiveIntegerField()
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='companies')

    def __str__(self):
        return '%s' % self.name


class Specialty(models.Model):
    code = models.CharField(primary_key=True, max_length=20)
    title = models.CharField(max_length=40)
    picture = models.ImageField(upload_to=MEDIA_SPECIALITY_IMAGE_DIR, default='150x150.gif')

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


class Application(models.Model):
    apply_id = models.AutoField(primary_key=True, db_column='id')
    written_username = models.CharField(max_length=128)
    written_phone = models.CharField(max_length=32)
    written_cover_letter = models.TextField()
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')

    def __str__(self):
        return '%s' % self.written_username
