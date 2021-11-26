from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from accounts.forms import SignupForm
from django.contrib.auth import views as auth_views
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from accounts.models import CustomUser


class SignupView(CreateView):
    form_class = SignupForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        customuser = form.save()
        login(self.request, customuser)
        self.object = customuser
        return HttpResponseRedirect(self.get_success_url())


class LoginView(auth_views.LoginView):
    template_name = 'registration/login.html'

login = LoginView.as_view()



class UserUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = CustomUser
    template_name = 'accounts/user_update.html'
    fields = ['username','introduce']
    success_url = 'user_trips'
    
    def test_func(self):
        user = self.request.user
        return user.id == self.kwargs['pk']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context
    
    def get_success_url(self):
        return reverse('user_trips', kwargs={'pk': self.object.id})