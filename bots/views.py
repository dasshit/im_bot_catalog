from django import forms

from django.contrib import auth
from django.contrib.auth.models import User

from django.shortcuts import render

from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect

# Create your views here.


class LoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'password']

        widgets = {
            # telling Django your password field in the mode is a password input on the template
            'password': forms.PasswordInput()
        }


def login(request: HttpRequest) -> HttpResponse:

    if not request.user.is_authenticated:

        login_form = LoginForm()

        return render(
            request=request,
            template_name='login.html',
            status=200,
            context={
                'form': login_form,
                'title': 'Login'
            }
        )
    else:
        return HttpResponseRedirect(
            redirect_to='/bots/list/'
        )


def logout(request: HttpRequest) -> HttpResponse:

    if request.user.is_authenticated:

        auth.logout(request)

    return HttpResponseRedirect(
        redirect_to='/bots/login/'
    )


def auth_form_check(request: HttpRequest) -> HttpResponse:

    username = request.POST['username']
    password = request.POST['password']

    user = auth.authenticate(request, username=username, password=password)

    if user is not None and user.is_active:

        auth.login(request, user)

        return HttpResponseRedirect(
            redirect_to='/bots/list/'
        )
    else:
        return HttpResponseRedirect(
            redirect_to='/bots/login/'
        )


def check_auth(func):
    def checking(request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(
                redirect_to='/bots/login/'
            )
        else:
            return func(request)
    return checking


@check_auth
def bots_list(request: HttpRequest) -> HttpResponse:

    return render(
        request=request,
        template_name='base.html',
        context={
            'title': 'Bots list',
            'links': [
                {
                    'href': '/bots/logout/', 'text': 'Logout'
                }
            ]
        }
    )
