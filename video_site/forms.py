from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='ユーザーID', max_length=100)
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput)
