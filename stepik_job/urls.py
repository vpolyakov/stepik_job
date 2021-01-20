"""stepik_job URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.contrib import admin
from django.urls import path, include, re_path

from job.views import custom_handler404, custom_handler500
from job.views import (
    MainView,
    DetailVacancyView,
    ListVacanciesView,
    ListSpecVacanciesView,
    ListCompanyVacanciesView,
)

handler404 = custom_handler404
handler500 = custom_handler500

urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),

    path('', MainView.as_view(), name='main'),
    path('vacancies/', ListVacanciesView.as_view(), name='vacancies'),
    re_path(r'^vacancies/cat/([\w-]+)/$', ListSpecVacanciesView.as_view(), name='spec_vacancies'),
    re_path(r'^companies/(\d{1,3})/$', ListCompanyVacanciesView.as_view(), name='company_vacancies'),
    path('vacancies/<int:pk>/', DetailVacancyView.as_view(), name='vacancy'),
]
