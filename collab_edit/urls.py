from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('home', views.home, name='home'),
    path('document/create/', views.document_create, name='document_create'),
    path('document/<int:doc_id>/', views.document_editor, name='document_editor'),
    path('ai-suggest/', views.ai_suggest, name='ai_suggest'),
    path('', views.login_view, name='login'),
    path('accounts/login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
