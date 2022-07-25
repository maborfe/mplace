from cProfile import label
from unittest.util import _MAX_LENGTH
from django import forms
from django.contrib.auth.models import User

class RegistrationForm(forms.Form):
  username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True,max_length=30, label='Usuario', error_messages={'invalid': 'Apenas letras e números'})))

  email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True,max_length=100)), label='Email')

  password = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True,max_length=10, render_value=False)), label='Password')

  password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True,max_length=10, render_value=False)), label='Password confirmation')

  def clean_username(self):
    try:
      user = User.objects.get(username__iexact=self.cleaned_data['username'])
    except User.DoesNotExist:
      return self.cleaned_data['username']
    raise forms.ValidationError('Esse usuário já existe')

  def clean(self):
    if 'password' in self.cleaned_data and \
      'password2' in self.cleaned_data:
      if self.cleaned_data['password'] != self.cleaned_data['password2']:
        raise forms.ValidationError('Passwords do not match')
    
    return self.cleaned_data

