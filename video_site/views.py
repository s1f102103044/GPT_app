from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone

from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm 

from django.contrib.auth.forms import UserCreationForm


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
	return render(request, 'video/top.html', {})

def question(request):
	return render(request, 'video/question.html')

def updated(request, article_id):
	return HttpResponse("article_id: {}".format(article_id))

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

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('top')
            else:
                messages.error(request, 'ユーザー名またはパスワードが間違っています')
    else:
        form = LoginForm()  # これがGETリクエスト時に必要です。
    return render(request, 'video/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('top')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "ユーザー登録が完了しました！ログインしてください。")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'video/register.html', {'form': form})