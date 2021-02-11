from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import SignupForm, LoginForm, TwoFactorForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from .models import User
from django.core.mail import EmailMessage
from . import timer
import threading


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            x = threading.Thread(target=timer.start_countdown, args=(User, user.pk, 0.5))
            x.start()
            return render(request, 'email_check.html', {'is_activated':False, 'is_link_invalid':False})
        else:
            form = SignupForm()
            return render(request, 'signup.html', {'form': form, 'is_user_exist':True})
    else:
        form = SignupForm()
        return render(request, 'signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        current_site = get_current_site(request)
        mail_subject = 'Вы успешно зарегистрированы'
        message = render_to_string('acc_done_email.html', {
            'domain': current_site.domain,
        })
        to_email = user.email
        email = EmailMessage(
                    mail_subject, message, to=[to_email]
        )
        email.send()
        return render(request, 'email_check.html', {'is_activated':True})
    else:
        return render(request, 'email_check.html', {'is_activated':False, 'is_link_invalid':True})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['email'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login or password')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')


def two_factor_login(request, uidb64, token):
    if request.method == 'POST':
        form = TwoFactorForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                uid = force_text(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)
            except(TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None
            if user is not None and account_activation_token.check_token(user, token):
                if user.is_active:
                    login(request, user)
                    print('logged in')
                    return redirect('/')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Wrong link')
    else:
        form = TwoFactorForm()
    return render(request, 'account/two_factor_login.html', {'form': form})

def profile_view(request):
    if request.user.is_authenticated:
        return render(request, 'profile.html', {'user':request.user})
    else:
        return HttpResponse('You are not logged in')