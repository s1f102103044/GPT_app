from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
    path('<int:article_id>/update', views.updated, name='updated'),
    path('hello', views.hello, name='hello'),
    path('redirect', views.redirect_test, name='redirect_test'),

    path('top',views.top,name='top'),
    path('question',views.question,name='question'),

    #あってるか微妙だが、GPT-3.5を動かすためのパスを書いた

    path('question/', views.question, name='question'),
]