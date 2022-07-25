from cProfile import label
from django import forms
from pkg_resources import require
from .models import Category, Product


""" class ProductForms(forms.Form):
  name = forms.CharField(max_length=255,
                        required=True, 
                        label = 'Nome',
                        widget=forms.TextInput(attrs={'class': 'form-control'}))

  
  quantity = forms.CharField(max_length=255,
                        required=True, 
                        label = 'Quantidade',
                        widget=forms.TextInput(attrs={'class': 'form-control'}))

  price = forms.CharField(max_length=255,
                        required=True, 
                        label = 'Valor',
                        widget=forms.TextInput(attrs={'class': 'form-control'}))

  short_description = forms.CharField(max_length=255,
                        required=True, 
                        label = 'Descrição Breve',
                        widget=forms.TextInput(attrs={'class': 'form-control'}))

  description = forms.CharField(max_length=255,
                        required=True, 
                        label = 'Descrição',
                        widget=forms.Textarea(attrs={'class': 'form-control'}))

  categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(),
                                                    label="Categoria(s)",
                                                    widget=forms.SelectMultiple(attrs={'class': 'form-control',
                                                    'style': 'height:140px' }))


   """

class ProductForms(forms.ModelForm):
    
    class Meta:
      
      model = Product

      exclude = ('slug', 'user')

      widgets = {
        'name': forms.TextInput(attrs={'class': 'form-control' }),
        'categories': forms.SelectMultiple(attrs={'class': 'form-control','style': 'height:120px'}),
        'quantity': forms.TextInput(attrs={'class': 'form-control'}),
        'price': forms.TextInput(attrs={'class': 'form-control'}),
        'short_description': forms.TextInput(attrs={'class': 'form-control'}),
        'description': forms.Textarea(attrs={'class': 'form-control', 'style': 'height: 100px;'}),	
      }

      labels = {
        'name': 'Nome',
        'categories': 'Categoria(s)',
        'quantity': 'Quantidade',
        'price': 'Preço',
        'short_description': 'Descrição Breve',
        'description': 'Descrição',
      }

class ProductQuestionForm(forms.Form):
  question = forms.CharField(
    label = 'Perguntar',
    widget=forms.Textarea(attrs={'class': 'form-control', 'id': 'question', 'placeholder': 'Faça sua pergunta'}),
    required=True
    )



class ProductAnswerForm(forms.Form):
  answer = forms.CharField(
    label = 'Responder',
    widget=forms.Textarea(attrs={'class': 'form-control', 'id': 'answer', 'style': 'height: 100px;','placeholder': 'Responder Pergunta'}),
    required=True
    )