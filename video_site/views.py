from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm 
from django.contrib.auth.forms import UserCreationForm

from .models import Conversation

from django.http import HttpResponseRedirect
from .forms import QuestionForm
import requests  # TMDb APIのリクエストに使用します

import openai

# 環境変数からAPIキーを読み込む
openai.api_key = 'B97dxwnrBS-KesXp2tuf62rF3D8AwQiaz9u437qpNa31D2bZglMJSXVKB4XgBwNg0F4Tzs6ON7bO_6Jv0ZF1WdQ'

def index(request):
    if request.user.is_authenticated:
        return redirect('top')
    else:
        return redirect('register')

def top(request):
    # セッションからユーザーの選択を取得する
    user_preferences = request.session.get('user_preferences')

    # TMDb APIを呼び出して映画のリストを取得する
    recommended_movies = []
    if user_preferences:
        api_key = 'e7f3afa7f6bc747e9a10789a5ca62773'
        genre = user_preferences.get('genre')
        url = f'https://api.themoviedb.org/3/discover/movie?api_key={api_key}&with_genres={genre}'
        response = requests.get(url)
        movies = response.json().get('results', [])
        recommended_movies = [{'title': movie['title'], 'image_url': movie['poster_path']} for movie in movies]
    else:
        movies = []

    return render(request, 'video/top.html', {'recommended_movies': recommended_movies})


def updated(request, article_id):
	return HttpResponse("article_id: {}".format(article_id))

def question(request):
    is_new_user = request.session.get('is_new_user', False)

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            user_input = form.cleaned_data.get('user_input')

            # OpenAI GPT-3に質問を送信して応答を取得
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": user_input}
                    ]
                )
                answer = response.choices[0].message['content']
            except Exception as e:
                answer = str(e)  # エラーメッセージをキャッチ

            # TMDb APIを呼び出して映画の推薦情報を取得
            api_key = 'e7f3afa7f6bc747e9a10789a5ca62773'
            url = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={user_input}'
            response = requests.get(url)
            movies = response.json().get('results', [])

            # 映画の推薦情報をセッションに保存
            request.session['recommended_movies'] = movies

            # ユーザーの好みをセッションに保存
            request.session['user_preferences'] = {
                'genre': user_input,  # ここではユーザー入力をジャンルとして扱う
                'director': '',  # 監督や俳優に関する情報は省略
                'actor': ''
            }

            # 新規ユーザーのマークを削除
            request.session['is_new_user'] = False

            return render(request, 'video/question.html', {'form': form, 'answer': answer, 'is_new_user': is_new_user})
    else:
        form = QuestionForm()

    return render(request, 'video/question.html', {'form': form, 'is_new_user': is_new_user})



def get_movies_data(genre, director, actor):
    api_key = 'e7f3afa7f6bc747e9a10789a5ca62773'
    # APIを使って映画データを取得するロジック
    # 例: ジャンルに基づいて映画を検索
    url = f'https://api.themoviedb.org/3/discover/movie?api_key={api_key}&with_genres={genre}'
    response = requests.get(url)
    movies = response.json().get('results', [])

    # 必要なデータ（タイトル、イメージURLなど）を抽出
    movies_data = [{'title': movie['title'], 'image_url': movie['poster_path']} for movie in movies]
    return movies_data


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('top')
            else:
                messages.error(request, 'ログイン情報が正しくありません。')
    else:
        form = LoginForm()
    return render(request, 'video/login.html', {'form': form})



@login_required
def user_logout(request):
    logout(request)
    return redirect('top')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            request.session['is_new_user'] = True
            return redirect('question')
    else:
        form = UserCreationForm()
    return render(request, 'video/register.html', {'form': form})



def save_conversation(request):
    if request.method == 'POST' and request.user.is_authenticated:
        user_input = request.POST.get('user_input')
        answer = request.POST.get('answer')
        content = f"User: {user_input}\nGPT: {answer}"
        Conversation.objects.create(user=request.user, content=content)
    return redirect('view_conversations')


def view_conversations(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    delete_mode = request.session.get('delete_mode', False)
    conversations = Conversation.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'video/conversations.html', {'conversations': conversations, 'delete_mode': delete_mode})

@login_required
def delete_conversations(request):
    if request.method == "POST":
        delete_ids = request.POST.getlist('delete_ids')
        Conversation.objects.filter(id__in=delete_ids, user=request.user).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def toggle_delete_mode(request):
    request.session['delete_mode'] = not request.session.get('delete_mode', False)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def format_response(text):
    # 「。」の後にHTMLの改行タグを追加
    formatted_text = text.replace("。", "。<br>")
    return formatted_text

def help(request):
    return render(request,'video/help.html')

def info(request):
    return render(request,'video/info.html')

def license(request):
    return render(request,'video/license.html')
