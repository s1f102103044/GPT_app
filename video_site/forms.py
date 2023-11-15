from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='ユーザーID', max_length=100)
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput)

class QuestionForm(forms.Form):
    # ここに質問に対するフィールドを定義します
    genre = forms.CharField(label='ジャンル', max_length=100)
    director = forms.CharField(label='監督', max_length=100)
    actor = forms.CharField(label='俳優', max_length=100)
    # その他必要なフィールドを追加...
    #new_user_question = forms.CharField(label='新規ユーザーの質問', max_length=100, required=False)