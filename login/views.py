from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from login.forms import RegistrationForm
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import logout as sair


def register(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      user = User.objects.create_user(username=form.cleaned_data.get('username'), email=form.cleaned_data.get('email'), password=form.cleaned_data.get('password'))
      return HttpResponseRedirect(reverse('register_success'))
  else:
    form = RegistrationForm()
    
  context = {'form': form}
  return render(request, 'registration/register.html', context)

def register_success(request):
  return render(request, 'registration/register_success.html')

