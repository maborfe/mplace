from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin
from django.contrib import admin

from .models import *

'''
  AJAX Admin Model

  Neste caso, serviu para facilitar as buscas dentro dos campos de categoria e usuario na 
  área administrativa. No campo é possível digitar o valor procurado e a pesquisa já vai
  mostrando os resultados 
  
'''

class CategoryAdmin(AjaxSelectAdmin):
  prepopulated_fields = {'slug': ('name', )}
  list_display = ('id', 'name', 'slug', 'order', 'hidden', 'parent')
  list_editable = ('hidden',)
  list_display_links = ('name', 'slug')
  list_filter = ['hidden']
  form = make_ajax_form(Category, {
    'parent': 'categories'
  })

admin.site.register(Category, CategoryAdmin)



class ProductAdmin(AjaxSelectAdmin):
  prepopulated_fields = {'slug': ('name', )}
  list_display = ('id','name', 'slug', 'price', 'short_description', 'status')
  list_editable = ('status',)
  list_display_links = ('id','name', 'slug')
  list_filter = ['name', 'categories']
  form = make_ajax_form(Product, {
    'user': 'user',
    'categories': 'categories',
  })


admin.site.register(Product, ProductAdmin)



class ProductAnswerInline(admin.StackedInline):
  model = ProductAnswer
  can_delete = False



class ProductQuestionAdmin(admin.ModelAdmin):
  list_display = ('id', 'product', 'question', 'status')
  list_display_links = ('id', 'product', 'question')

  inlines = (ProductAnswerInline,)

admin.site.register(ProductQuestion, ProductQuestionAdmin)

