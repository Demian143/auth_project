from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def signin(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(email=email)

        if user:
            return HttpResponse('User already exists.')

        user = User.objects.create_user(
            username=name, email=email, password=password)
        user.save()

        return HttpResponseRedirect(reverse('authentication:user_home'))

    else:
        return render(request, 'authentication/signin.html', context={})


def user_login(request):
    if request.method == 'POST':
        name = request.POST['name']
        password = request.POST['password']

        user = authenticate(request, username=name, password=password)

        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('authentication:user_home'))

        else:
            return HttpResponse('Something wrong, try again.')

    else:
        return render(request, 'authentication/login.html')


def user_logout(request):
    # will be used in the loged page
    logout(request)
    return HttpResponseRedirect(reverse('authentication:user_home'))


@login_required(login_url='/authentication/login/')
def user_home_page(request):
    """Home page with references to the following actions:
            Update one of the data about the user (password, username and email).
            Delete the account."""

    return render(request, 'authentication/user_homepage.html')


@login_required(login_url='/authentication/login/')
def delete_account(request):
    """ The name explains itself. """
    if request.method == 'POST':
        password = request.POST['password1'] == request.POST['password2']

        if password is True:
            user = User.objects.get(username=request.user.get_username())
            user.delete()
            return HttpResponseRedirect(reverse('authentication:user_home'))

        return HttpResponse('One of the fields is wrong. Try again.')

    else:
        return render(request, 'authentication/delete_account.html')


@login_required(login_url='/authentication/login/')
def update_password(request):
    # confirm if old password is correct
    # confirm if new password 1 and 2 are equal
    # if correct, success
    if request.method == 'POST':
        new_password = request.POST['new_password1'] == request.POST['new_password2']
        user = authenticate(username=request.user.get_username(),
                            password=request.POST['old_password'])

        if new_password is True and user:
            new_password = request.POST['new_password1']
            # user = User.objects.get(username=request.user.get_username())
            user.set_password(new_password)
            user.save()

            return HttpResponseRedirect(reverse('authentication:user_home'))

        else:
            return HttpResponse('Something went wrong.')

    else:
        return render(request, 'authentication/update_password.html')


@login_required(login_url='/authentication/login/')
def update_username(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.user.get_username(
        ), password=request.POST['password'])

        if user:
            user = User.objects.get(username=request.user.get_username())
            user.username = request.POST['new_username']
            user.save()

            return HttpResponseRedirect(reverse('authentication:user_home'))
    else:
        return render(request, 'authentication/update_username.html')


@login_required(login_url='/authentication/login/')
def update_email(request):
    if request.method == 'POST':
        new_email = request.POST['new_email'] == request.POST['confirm_new_email']
        user = authenticate(username=request.user.get_username(),
                            password=request.POST['password'])

        if user and new_email is True:
            user = User.objects.get(username=request.user.get_username())
            user.email = request.POST['new_email']
            user.save()

            return HttpResponseRedirect(reverse('authentication:user_home'))

        return HttpResponse('One of the fields is wrong.')

    else:
        return render(request, 'authentication/update_email.html')
