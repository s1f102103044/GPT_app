from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone

import openai


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

def top(request):
	return render(request, 'video/top.html')

def question(request):
	return render(request, 'video/question.html')

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



	from django.shortcuts import render





def question(request):
    openai.api_key = 'Z98YF2NKSzzNbpc6NkvpUjckblBR4X3XdZJAMRgw6kzA_uIBE3ajapjdg_sRPx4qjB0NQY5ZjPQNlhudzOKM2zg'
    openai.api_base = "https://api.openai.iniad.org/api/v1"
    answer = ""
    if request.method == "POST":
        user_input = request.POST.get("user_input")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "あなたは映画をおすすめするアシスタントです。次の要求に具体的に答えてください。"},
                {"role": "user", "content": user_input}
            ],
        )
        answer = response.choices[0].message['content']
    return render(request, "video/question.html", {"answer": answer})
