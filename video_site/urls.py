from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
    path('<int:article_id>/update', views.updated, name='updated'),
    path('hello', views.hello, name='hello'),
    path('redirect', views.redirect_test, name='redirect_test'),
    path('<int:article_id>/', views.detail, name='detail'),
    path('<int:atricle_id>/delete', views.delete, name='delete'),
    path('<int:article_id>/update', views.update, name='update'),

    #あってるか微妙だが、GPT-3.5を動かすためのパスを書いた
    path('gpt', views.gpt35, name='gpt35'),
]