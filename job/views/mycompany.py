from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView
from django.views.generic.edit import CreateView

from job.forms import MyCompanyForm
from job.models import Company


@method_decorator(login_required, name='dispatch')
class MycompanyView(FormView):
    template_name = 'job/company-edit.html'
    form_class = MyCompanyForm
    success_url = '/mycompany'

    def get(self, request, *args, **kwargs):
        if Company.objects.filter(owner=self.request.user):
            form = self.form_class(instance=Company.objects.get(owner=self.request.user))
            return render(request, self.template_name, {'form': form})
        else:
            return redirect('/mycompany/letsstart/')

    def post(self, request, *args, **kwargs):
        owner = self.request.user
        comp = get_object_or_404(Company, owner=owner)
        form = self.form_class(request.POST, instance=comp)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = owner
            post.save()
            return redirect('/mycompany/')


@method_decorator(login_required, name='dispatch')
class MycompanyCreateView(LoginRequiredMixin, CreateView):
    form_class = MyCompanyForm
    success_url = '/mycompany/'
    template_name = 'job/company-edit.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class MycompanyLetsStartView(TemplateView):
    template_name = 'job/company-create.html'
