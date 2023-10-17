from django.urls import path
from . import views

urlpatterns = [
	#path('', views.index, name='index'),
    #path('<int:article_id>/update', views.updated, name='updated'),
    #path('hello', views.hello, name='hello'),
    #path('redirect', views.redirect_test, name='redirect_test'),
    
    path('top',views.top,name='top'),
    path('question',views.question,name='question'),

    #あってるか微妙だが、GPT-3.5を動かすためのパスを書いた

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