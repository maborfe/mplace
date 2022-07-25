from django.urls import path
from . import views as v
from django.contrib.auth import views

urlpatterns = [ 
  path('register/', v.register, name='register'),
  path('register/success', v.register_success, name='register_success'),
  path('login/', views.LoginView.as_view(),name='login'),
  path('logout/', views.LogoutView.as_view(next_page='/'), name='logout'),
]