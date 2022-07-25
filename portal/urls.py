from django.urls import include, path, re_path

from portal.models import Product

from . import views

urlpatterns = [
  # HOME
  path('', views.home, name='home'),

  #  BUSCA
  path('search_category/<int:id>', views.search_category, name='search_category'),
  path('search', views.search, name='search'),

  #  LISTA ANUNCIOS
  path('products', views.productList, name='products'),
  
  #  ADICIONA ANUNCIO (PELA LISTA DE ANUNCIOS)
  path('products/new', views.addProduct, name='addProduct'),

  # EDITA ANUNCIO (PELA LISTA DE ANUNCIOS)
  path('products/edit/<int:id_anuncio>', views.editProduct, name='editProduct'),

  #  DESATIVA E ATIVA ANUNCIOS NA LISTA DE ANUNCIOS
  path('products/desativar/<int:id_anuncio>', views.desativar, name='desativar'),
  path('products/ativar/<int:id_anuncio>', views.ativar, name='ativar'),
  
  #  EXIBE DETALHE DO ANUNCIO
  path('products/<slug:slugid>' , views.show, name='show'),

  #  ADICIONA PERGUNTAS, LISTA PERGUNTAS DO ANUNCIO X, RESPONDE PERGUNTAS DO ANUNCIO X
  path('products/new/question/<int:id_anuncio>', views.product_question, name = 'product_question'),
  path('products/<int:id_anuncio>/questions', views.question_list, name='question_list'),
  path('products/question/responder/<int:id_question>', views.responder, name = 'responder'),
]
