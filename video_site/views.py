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
import json

#import logging

#logger = logging.getLogger(__views.py__)  # __name__は現在のファイル名（モジュール名）になります


def index(request):
    if request.user.is_authenticated:
        return redirect('top')
    else:
        return redirect('register')

def top(request):
    recommended_movies = request.session.get('recommended_movies', [])
    return render(request, 'video/top.html', {'recommended_movies': recommended_movies})    

'''
def top(request):
    # セッションからユーザーの選択を取得する
    # TMDb APIを呼び出して映画のリストを取得する
    recommended_movies = request.session.get('recommended_movies', [])
    
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
'''

def updated(request, article_id):
	return HttpResponse("article_id: {}".format(article_id))


'''
def question(request):
    openai.api_key = 'B97dxwnrBS-KesXp2tuf62rF3D8AwQiaz9u437qpNa31D2bZglMJSXVKB4XgBwNg0F4Tzs6ON7bO_6Jv0ZF1WdQ'
    openai.api_base = "https://api.openai.iniad.org/api/v1"
    answer = ""
    

    try:
        if request.method == "POST":
            user_input = request.POST.get("user_input")
            # GPT-4に質問を送信して応答を取得
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "あなたは映画をおすすめするアシスタントです。次の要求に具体的に答えてください。"},
                    {"role": "user", "content": user_input}
                ]
            )
            answer = response.choices[0].message['content']

    except Exception as e:
        answer = str(e)  # エラーメッセージをキャッチ
        
    if request.method == 'GET' or not form.is_valid():
        form = QuestionForm()
        return render(request, 'video/question.html', {'form': form, 'answer': answer})
        
    return render(request, 'video/question.html', {'answer': answer})
'''










#ここからquestion関係の関数!!








def extract_search_parameters(response):
    try:
        # GPT-4の応答をJSONオブジェクトに変換
        response_data = json.loads(response)

        # 応答から必要なデータを抽出
        genre = response_data.get('genre', None)
        director = response_data.get('director', None)
        actor = response_data.get('actor', None)

        # 抽出したデータを辞書形式で返す
        return {
            'genre': genre,
            'director': director,
            'actor': actor
        }
    except json.JSONDecodeError:
        # JSON形式でない場合のエラーハンドリング
        return {'genre': None, 'director': None, 'actor': None}







def get_person_id(name):
    """ 人物の名前からTMDbのIDを取得する関数 """
    base_url = 'https://api.themoviedb.org/3/search/person'
    api_key = 'e7f3afa7f6bc747e9a10789a5ca62773'
    params = {
        'api_key': api_key,
        'query': name
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        results = response.json().get('results', [])
        if results:
            # 最初の検索結果のIDを返す
            return results[0]['id']
    return None










def get_movies_data(genre=None, director=None, actor=None, language='ja-JP', page=1, query=None, year=None, primary_release_year=None, sort_by=None, include_adult=False, append_to_response=None, certification_country=None, certification=None):
    print("get_movies_data 関数が呼び出されました")
    base_url = 'https://api.themoviedb.org/3/discover/movie'
    api_key= 'e7f3afa7f6bc747e9a10789a5ca62773'
    
    # 人物のIDを取得
    director_id = get_person_id(director) if director else None
    actor_id = get_person_id(actor) if actor else None

    
    
    genre_ids={'Action': 28, 'Adventure': 12, 'Animation': 16, 'Comedy': 35, 'Crime': 80, 'Documentary': 99, 'Drama': 18, 'Family': 10751, 'Fantasy': 14, 'History': 36, 'Horror': 27, 'Music': 10402, 'Mystery': 9648, 'Romance': 10749, 'Science Fiction': 878, 'TV Movie': 10770, 'Thriller': 53, 'War': 10752, 'Western': 37}
    # パラメータの入力
    # genre_idsから指定したジャンル名に対応するIDを取り出します
    genre_id = genre_ids.get(genre)

    if genre_id is not None:
        print(f"{genre}のIDは{genre_id}です。")
    else:
        print(f"{genre}は見つかりませんでした。")

    params = {
        'api_key': 'e7f3afa7f6bc747e9a10789a5ca62773',
        'with_genres': genre,
        'with_crew': director_id,
        'with_cast': actor_id,
        'language': language,
        'page': page,
        'query': query,
        'year': year,
        'primary_release_year': primary_release_year,
        'sort_by': sort_by,
        'include_adult': include_adult,
        'append_to_response': append_to_response,
        'certification_country': certification_country,
        'certification': certification,
    }

    response = requests.get(base_url, params=params)
    url = response.url

    print(url)
    
    try:
        response = requests.get(url)

        # ステータスコードをチェック
        if response.status_code == 200:
            movies = response.json().get('results', [])

            # 必要なデータ（タイトル、イメージURLなど）を抽出
            movies_data = []
            for movie in movies:
                title = movie.get('title', 'タイトル不明')
                image_path = movie.get('poster_path', '')
                image_url = f"https://image.tmdb.org/t/p/w500{image_path}" if image_path else None
                movies_data.append({'title': title, 'image_url': image_url})

            return movies_data
        else:
            print("APIリクエストが失敗しました: ステータスコード", response.status_code)
            return []
    except Exception as e:
        print("APIリクエスト中にエラーが発生しました:", e)
        return []
        

# 例として、ジャンル、監督、俳優を指定して映画データを取得する
movies_data = get_movies_data(genre='Action', actor='Robert Downey Jr.')
print(movies_data)









def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True








def question(request):
    print("question ビューが呼び出されました")
    openai.api_key = 'Z98YF2NKSzzNbpc6NkvpUjckblBR4X3XdZJAMRgw6kzA_uIBE3ajapjdg_sRPx4qjB0NQY5ZjPQNlhudzOKM2zg'
    openai.api_base = "https://api.openai.iniad.org/api/v1"
    answer = ""

    try:
        if request.method == "POST":
            user_input = request.POST.get("user_input")
            print("ユーザー入力:", user_input)


            # GPT-4に質問を送信して応答を取得
            prompt = "ユーザーからの質問: {}\n\n".format(user_input) + \
                "ユーザーが映画の推薦を求めている場合、以下のJSON形式で映画の推薦に必要な情報を提供してください。それ以外の質問には通常のテキスト応答を行ってください。\n" + \
                "映画の推薦が要求された場合、モデルは映画のタイトル、ジャンル、監督、主要俳優をJSON形式で提供する必要があります。\n" + \
                "JSON応答の例:\n" + \
                "{\n" + \
                "  \"title\": \"映画のタイトル\",\n" + \
                "  \"genre\": \"ジャンル\",\n" + \
                "  \"director\": \"監督の名前\",\n" + \
                "  \"actor\": \"主要俳優の名前\"\n" + \
                "}\n"
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "あなたは映画をおすすめするアシスタントです。次の要求に具体的に答えてください。"},
                    {"role": "user", "content": user_input}
                ]
            )
            answer = response.choices[0].message['content']
            print("GPT-4からの応答:", answer)


            # GPTの解答から取得すべき映画の特徴を取得しTMDbから持ってくる
            if is_json(answer):
                print("応答はJSON形式です")
                search_params = extract_search_parameters(answer)
                print("抽出された検索パラメータ:", search_params)
                movies_data = get_movies_data(search_params['genre'], search_params['director'], search_params['actor'])
                print("取得された映画データ:", movies_data)
                # 映画データに完全な画像URLを追加
                base_image_url = "https://image.tmdb.org/t/p/w500"
                for movie in movies_data:
                    if movie['image_path']:
                        movie['image_url'] = base_image_url + movie['image_path']
                    else:
                        movie['image_url'] = None  # 画像がない場合
                        
                answer += "\n映画の推薦: " + str(movies_data)

                
                # TMDbの映画データをGPTに整理してもらう
                organized_data = organize_data_with_gpt4(movies_data)
                answer = organized_data
                        
                # Djangoテンプレートにデータを渡す
                return render(request, 'video/question.html', {'movies_data': movies_data})
            
                
            else:
                print("応答はJSON形式ではありません")


    except Exception as e:
        print("エラー発生:", e)
        answer = str(e)  # エラーメッセージをキャッチ

    return render(request, 'video/question.html', {'answer': answer})












#ここまでquestion関係の関数!!













'''
def question(request):
    is_new_user = request.session.get('is_new_user', False)
    print("Is new user:", is_new_user)  # デバッグ情報

    if request.method == 'POST':
        print("Received POST request")  # デバッグ情報
        form = QuestionForm(request.POST)
        if form.is_valid():
            print("Form is valid")  # デバッグ情報
            user_input = form.cleaned_data.get('user_input')
            print("User input:", user_input)  # デバッグ情報

            # OpenAI GPT-4に質問を送信
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4-32k-0613",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": user_input}
                    ]
                )
                answer = response.choices[0].message['content']
                print("GPT-4 response:", answer)  # デバッグ情報
            except Exception as e:
                answer = str(e)
                print("GPT-4 error:", answer)  # デバッグ情報

            # TMDb APIを呼び出し
            try:
                api_key = 'e7f3afa7f6bc747e9a10789a5ca62773'
                url = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={user_input}'
                response = requests.get(url)
                movies = response.json().get('results', [])
                print("Movies data:", movies)  # デバッグ情報
            except Exception as e:
                print("TMDb API error:", str(e))  # デバッグ情報

            # セッションに情報を保存
            request.session['recommended_movies'] = movies
            request.session['user_preferences'] = {
                'genre': user_input,
                'director': '',
                'actor': ''
            }

            request.session['is_new_user'] = False
            return render(request, 'video/question.html', {'form': form, 'answer': answer, 'is_new_user': is_new_user})
        else:
            print("Form errors:", form.errors)  # デバッグ情報
    else:
        form = QuestionForm()
        print("GET request - New form")  # デバッグ情報

    return render(request, 'video/question.html', {'form': form, 'is_new_user': is_new_user})
'''
from django.shortcuts import render, redirect
from .forms import QuestionForm
import requests
#e7f3afa7f6bc747e9a10789a5ca62773
def fetch_movies(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            genre = form.cleaned_data['genre']
            director = form.cleaned_data['director']
            actor = form.cleaned_data['actor']
            
            api_key = 'e7f3afa7f6bc747e9a10789a5ca62773'
            params = {
                'api_key': api_key,
                'language': 'ja-JP',
                'query': genre,
                'include_adult': 'false'
            }
            
            response = requests.get('https://api.themoviedb.org/3/search/movie', params=params)
            if response.status_code == 200:
                movies_data = response.json().get('results', [])
                request.session['recommended_movies'] = movies_data
                return redirect('top')
            else:
                # Handle errors here
                print("Error fetching movies:", response.status_code)

    # If not POST method or form is not valid, show the form again with errors
    else:
        form = QuestionForm()
    if request.method == 'GET' or not form.is_valid():
        form = QuestionForm()
        return render(request, 'video/question.html', {'form': form})
    return render(request, 'video/question.html', {'form': form})


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
