
from django.contrib import admin
from django.urls import path
from . import views
from user.views import register_view
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('',views.homepage,name='home'),
    path('contact/', views.contact, name='contact'),
    path('signup/',register_view, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('loc_admin/',views.adm, name='adm_panel'),
]
