from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone

import openai
openai.api_key = 'B97dxwnrBS-KesXp2tuf62rF3D8AwQiaz9u437qpNa31D2bZglMJSXVKB4XgBwNg0F4Tzs6ON7bO_6Jv0ZF1WdQ'
openai.api_bace = 'https://api.openai.iniad.org/api/v1'

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

#以下がGPT-3.5をPythonで実行するための関数
#なお、本番運用時にGPT-3.5ではなくGPT-4のAPIキーに変更予定（上記「openai.api_key」を変更する）
def gpt35():
	question = input('Question:')

	response = openai.ChatCompletion.create(
		model = 'gpt-3.5-turbo',
		message=[
			{'role':'user','content':question},
		],
	)
	print(response['choices'][0]['message']['content'])


def question(request):
    answer = ""
    if request.method == "POST":
        user_input = request.POST.get("user_input")
        openai.api_key = 'B97dxwnrBS-KesXp2tuf62rF3D8AwQiaz9u437qpNa31D2bZglMJSXVKB4XgBwNg0F4Tzs6ON7bO_6Jv0ZF1WdQ'
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=user_input,
            max_tokens=300
        )
        answer = response.choices[0].text
    return render(request, "video/question.html", {"answer": answer})