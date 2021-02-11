from django.shortcuts import render
from django.http import HttpResponse
from .forms import PartnerForm, CallMeForm, CompanyForm
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

def home_view(request, *args, **kwargs):
    if request.method == 'POST':
        print(request.POST)
        if 'phone_sub' in request.POST:
            form = CallMeForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                mail_subject = 'Rostishka_team Просьба связаться'
                message = render_to_string('call_me_email.html',{
                    'phone':cd['phone']
                })
                to_email = 'vlad.los77712@gmail.com'
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                return HttpResponse('email send')
            else:
                return HttpResponse('form was not validated')
        elif 'company' in request.POST:
            form = CompanyForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                mail_subject = 'Rostishka_team Просьба связаться'
                message = render_to_string('company_email.html',{
                    'contact':cd['contact'],
                    'location':cd['location'],
                    'size':cd['warehouse_size'],
                    'company':cd['company'],
                })
                to_email = 'vlad.los77712@gmail.com'
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                return HttpResponse('email send')
            else:
                return HttpResponse('form was not validated')
    else:
        companyForm = CompanyForm()
        phoneForm = CallMeForm()
        return render(request, "home.html", {'user':request.user, 'phoneForm':phoneForm, 'companyForm':companyForm,})
        

def about_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = PartnerForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            mail_subject = 'Rostishka_team Новый фидбек'
            message = render_to_string('new_partner_email.html',{
                'email':cd['email'],
                'name':cd['name'],
                'message':cd['message']
            })
            to_email = 'vlad.los77712@gmail.com'
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('email send')
        else:
            return HttpResponse('form was not validated')
    else:
        return render(request, "about.html", {'form':PartnerForm()})


def warehouse_view(request, *args, **kwargs):
    return render(request, "warehouse.html", {})

def schedule_view(request, *args, **kwargs):
    return render(request, "schedule.html", {})

def stream_view(request, *args, **kwargs):
    stream_url = 'https://www.youtube.com/embed/7qXQ75fSd6s'
    return render(request, "stream.html", {'stream_url':stream_url, 'is_admin':request.user.is_admin})