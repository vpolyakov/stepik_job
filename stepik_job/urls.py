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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include

from accounts.views import UserLoginView, UserSignupView
from job.views.mycompany import MycompanyView, MycompanyCreateView, MycompanyLetsStartView
from job.views.myvacancies import MyCompVacanciesView, \
    MyCompVacancyCreateView, MyCompVacancyUpdateView, MyCompVacancyLetsStartView
from job.views.public import (
    MainView,
    DetailVacancyView,
    ListVacanciesView,
    ListSpecVacanciesView,
    ListCompanyVacanciesView,
    VacancySendView,

)
from job.views.public import custom_handler404, custom_handler500

handler404 = custom_handler404
handler500 = custom_handler500

urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),

    path('', MainView.as_view(), name='main'),
    path('vacancies/', ListVacanciesView.as_view(), name='vacancies'),
    path('vacancies/cat/<slug:code>/', ListSpecVacanciesView.as_view(), name='spec_vacancies'),
    path('companies/<int:pk>/', ListCompanyVacanciesView.as_view(), name='company_vacancies'),
    path('vacancies/<int:pk>/', DetailVacancyView.as_view(), name='vacancy'),

    path('vacancies/<int:vacancy_id>/send/', VacancySendView.as_view(), name='vacancy_send'),

    path('mycompany/', MycompanyView.as_view(), name='mycompany'),
    path('mycompany/create/', MycompanyCreateView.as_view(), name='mycompany_create'),
    path('mycompany/letsstart/', MycompanyLetsStartView.as_view(), name='my_company_lets_start'),

    path('mycompany/vacancies/', MyCompVacanciesView.as_view(), name='mycompany_vacancies'),
    path('mycompany/vacancies/<int:pk>/', MyCompVacancyUpdateView.as_view(), name='mycompany_vacancy'),
    path('mycompany/vacancies/create/', MyCompVacancyCreateView.as_view(), name='mycompany_vacancies_create'),
    path('mycompany/vacancies/letsstart/', MyCompVacancyLetsStartView.as_view(), name='mycompany_vacancies_letsstart'),

    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserSignupView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
