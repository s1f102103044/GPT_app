from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone

def index(request):
	context = {
        "articles": [
            {
                "id": 1,
                "title": "Post 01",
                "body": "test post.\nLorem ipsum dolor sit amet, \nconsectetur adipiscing elit,\n sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.\n", 
                "posted_at": timezone.now # option
            }
        ]
    }
	return render(request, 'video/index.html', context)

def updated(request, article_id):
	return HttpResponse("article_id: {}".format(article_id))

def hello(request):
    data = {
	    'name':'Alice',
	    'weather':'CLOUDY',
	    'weather_detail':['Temperature: 23℃', 'Humidity: 40%', 'Wind: 5m/s'],
	    'isGreatFortune': True,
	    'fortune':'Great Fortune!'
    }
    return render(request, 'video/hello.html', data)

def redirect_test(request):
	return redirect(hello)

def detail(request, article_id):
	context = {
		"article_id": article_id
    }
	return render(request, "video/tbd.html", context)

def update(request, article_id):
	context = {
		"article_id":article_id
    }
	return render(request, "video/tbd.html", context)

def delete(request, article_id):
	return redirect(index)