from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import SignupForm, LoginForm, TwoFactorForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from .models import User
from django.core.mail import EmailMessage
from . import timer
import threading
from random import randint
import re

def parse_email(s):
    (_, _, _, raw_email, _) = s.split(' ', 4)
    email = raw_email.replace('value="', '')
    email = email.rstrip('"')
    return email


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        email = parse_email(str(form['email']))
        try:
            user = User.objects.get(email=email)
            form = SignupForm()
            return render(request, 'signup.html', {'form': form, 'is_user_exist':True})
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
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
            x = threading.Thread(target=timer.start_countdown, args=(User, user.pk, 15))
            x.start()
            return render(request, 'email_check.html', {'is_activated':False, 'is_link_invalid':False})
                
        else:
            form = SignupForm()
            return render(request, 'signup.html', {'form': form, 'is_user_exist':False, 'not_validated':True})
            
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

def get_code():
    code = ''
    for i in range(10):
        num = randint(0, 9)
        code += str(num)
    return code

def user_login(request):
    print('login')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['email'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    code = get_code()
                    user.code = code
                    user.save()
                    mail_subject = 'Код аутентификации'
                    message = render_to_string('two_factor_email.html', {'code':code})
                    to_email = user.email
                    email = EmailMessage(
                        mail_subject, message, to=[to_email]
                    )
                    email.send()
                    current_site = get_current_site(request)
                    domain = current_site.domain
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    token = account_activation_token.make_token(user)
                    # login(request, user)
                    print('http://' + domain + '/account/code/' + 'uidb64=' + uid + 'token=' + token)
                    return redirect('http://' + domain + '/account/code/' + uid + '/' + token + '/')
                else:
                    return render(request, 'account/login.html', {'form': form, 'disabled':True, 'not_validated':False})
            else:
                return render(request, 'account/login.html', {'form': form, 'disabled':False, 'not_validated':True})
    else:
        form = LoginForm()
        return render(request, 'account/login.html', {'form': form, 'disabled':False, 'not_validated':False})

def user_logout(request):
    logout(request)
    return redirect('home')


def two_factor_login(request, uidb64, token):
    if request.method == 'POST':
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        form = TwoFactorForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            print(user.email)
            if user is not None:
                if user.code == cd['code']:
                    login(request, user)
                    return redirect('home')
                else:
                    return render(request, 'two_factor_login.html', {'form': form, 'wrong_code':True })
    else:
        form = TwoFactorForm()
        return render(request, 'two_factor_login.html', {'form': form, 'wrong_code':False})

def profile_view(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
            email = parse_email(str(u_form['email']))
            try:
                user = User.objects.get(email=email)
                if not user == request.user:
                    print('exist')
                    u_form = UserUpdateForm(instance=request.user)
                    p_form = ProfileUpdateForm(instance=request.user.profile)
                    return render(request, 'profile.html', {'user':request.user, 'u_form':u_form, 'p_form':p_form, 'email_busy':True})
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None
            if u_form.is_valid() and p_form.is_valid():
                print('valid')
                u_form.save()
                p_form.save()
                messages.success(request, f'Your account has been updated!')
                return redirect('profile')
        else:
            print('meh')
            u_form = UserUpdateForm(instance=request.user)
            p_form = ProfileUpdateForm(instance=request.user.profile)
            return render(request, 'profile.html', {'user':request.user, 'u_form':u_form, 'p_form':p_form, 'email_busy':False})
    else:
        return HttpResponse('You are not logged in')