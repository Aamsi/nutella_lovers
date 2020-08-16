from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


from .forms import SignUpForm, SigninForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('welcome')
    else:
        form = SignUpForm()
    return render(request, 'user/signup.html', {'form': form})

@login_required(login_url='/account/login/')
def signout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('welcome')

def signin(request):
    errors = None
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            print(email)
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            print(user)
            if user:
                login(request, user)
                return redirect('welcome')
            else:
                errors = "Mauvais identifiants, veuillez réessayer"
        else:
            errors = "Une erreur a eu lieu, veuillez réessayer"
    else:
        form = SigninForm()
    return render(request, 'user/signin.html', {'form': form, 'errors': errors})

@login_required(login_url='/account/login/')
def my_account(request):
    return render(request, 'user/myaccount.html')