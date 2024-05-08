from django import forms


class LoginUserForm(forms.Form):
    user_name = forms.CharField(label='Логин',
                                widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-input'}))

