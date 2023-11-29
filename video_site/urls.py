from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.register, name='register'), 

    path('top',views.top,name='top'),
    path('question',views.question,name='question'),
    path('question/', views.question, name='question'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('register/', views.register, name='register'),
    path('save_conversation/', views.save_conversation, name='save_conversation'),
    path('view_conversations/', views.view_conversations, name='view_conversations'),
    path('toggle_delete_mode/', views.toggle_delete_mode, name='toggle_delete_mode'),
    path('delete_conversations/', views.delete_conversations, name='delete_conversations'),
    path('question/', views.question, name='question_page'),
]