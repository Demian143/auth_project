from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import SignInForm, LoginForm, DeleteAccountForm
from django.views import View
from django.views.generic import TemplateView


class SignInView(View):
    def get(self, request):
        form = SignInForm()
        return render(request, 'authentication/signin.html', context={'form': form})

    def post(self, request):
        form = SignInForm(request.POST)
        if form.is_valid():
            user = User.objects.filter(email=request.POST.get('email'))

            if user:
                return HttpResponse('User already exists.')

            user = User.objects.create_user(
                username=request.POST.get('name'),
                email=request.POST.get('email'),
                password=request.POST.get('password')
            )
            user.save()

            return HttpResponseRedirect(reverse('authentication:user_home'))


class LoginView(View):

    def get(self, request):
        form = LoginForm()
        return render(request,
                      'authentication/login.html',
                      context={'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            name = request.POST.get('name')
            password = request.POST.get('password')

            user = authenticate(request, username=name, password=password)

            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('authentication:user_home'))

            else:
                return HttpResponse('Something wrong, try again.')


def user_logout(request):
    # will be used in the loged page
    logout(request)
    return HttpResponseRedirect(reverse('authentication:user_home'))


@method_decorator(login_required(login_url='/authentication/login/'), name='dispatch')
class UserHomeView(TemplateView):
    template_name = 'authentication/user_homepage.html'


@method_decorator(login_required(login_url='/authentication/login/'), name='dispatch')
class DeleteAccountView(View):
    def get(self, request):
        form = DeleteAccountForm()
        return render(request, 'authentication/delete_account.html', context={'form': form})

    def post(self, request):
        form = DeleteAccountForm(request.POST)

        if form.is_valid():

            if request.POST.get('password') == request.POST.get('confirm_password'):
                user = User.objects.get(username=request.user.get_username())
                user.delete()
                return HttpResponseRedirect(reverse('authentication:user_home'))

            return HttpResponse('One of the fields is wrong. Try again.')


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
