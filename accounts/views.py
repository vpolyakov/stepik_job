# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView

from accounts.forms import MyUserCreationForm


# Create your views here.
class UserSignupView(CreateView):
    form_class = MyUserCreationForm
    success_url = '/login'
    template_name = 'accounts/register.html'


class UserLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'accounts/login.html'
    # authentication_form = LoginForm
