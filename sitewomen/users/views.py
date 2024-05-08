from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy

from users.forms import LoginUserForm


def login_user(request):
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            print(cd)
            user = authenticate(request, username=cd['user_name'],
                                password=cd['password'])
            if user and user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse_lazy('home'))
    else:
        form = LoginUserForm()
    return render(request, 'users/login.html', {'form': form})


def logout_user(request):
    logout(request)

    return HttpResponseRedirect(reverse_lazy('users:login'))



