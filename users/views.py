from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .decorators import unauthenticated_user


@unauthenticated_user
def register_page(request):
    # instance of custom user form CreateUserForm
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            # get username from form data
            user = form.cleaned_data.get('username')
            # send success message
            messages.success(request, 'Account was created for ' + user)
            return redirect('users:login')

    context = {'form': form}
    return render(request, "users/register.html", context)


@unauthenticated_user
def login_page(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # if user is successfully authenticated
            login(request, user)
            return redirect("menu:product_list")
        else:
            # else send a info message
            messages.info(request, "Username or password is incorrect")

    return render(request, "users/login.html")


@login_required(login_url='/auth/login')
def logout_user(request):
    logout(request)
    return redirect("menu:product_list")
