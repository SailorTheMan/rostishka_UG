from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from .forms import PartnerForm, CallMeForm, CompanyForm
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .db_connector import get_schedule, get_warehouse, get_report, get_database
from accounts.models import User


def home_view(request, *args, **kwargs):
    if request.method == 'POST':
        if 'phone_sub' in request.POST:
            form = CallMeForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                mail_subject = 'Rostishka_team Просьба связаться'
                message = render_to_string('call_me_email.html',{
                    'phone':cd['phone']
                })
                emails = User.objects.filter(is_superuser=True).values_list('email')
                to_email = []
                for row in emails:
                    to_email.append(row[0])
                email = EmailMessage(
                    mail_subject, message, to=to_email
                )
                email.send()
                return render(request, 'form_sent.html', {'success': True})
            else:
                return render(request, 'form_sent.html', {'success': False})
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
                emails = User.objects.filter(is_superuser=True).values_list('email')
                to_email = []
                for row in emails:
                    to_email.append(row[0])
                email = EmailMessage(
                    mail_subject, message, to=to_email
                )
                email.send()
                return render(request, 'form_sent.html', {'success': True})
            else:
                return render(request, 'form_sent.html', {'success': False})
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
            emails = User.objects.filter(is_superuser=True).values_list('email')
            to_email = []
            for row in emails:
                to_email.append(row[0])
            email = EmailMessage(
                mail_subject, message, to=to_email
            )
            email.send()
            return render(request, 'form_sent.html', {'success': True})
        else:
            return render(request, 'form_sent.html', {'success': False})
    else:
        return render(request, "about.html", {'form':PartnerForm()})


def warehouse_view(request, *args, **kwargs):
    empty_count, warehouse = get_warehouse()
    model_count, manuf_count, date_count, database = get_database()
    print(model_count)
    return render(request, "warehouse.html", {
        'warehouses':warehouse,
        'empty_count':empty_count,
        'database':database,
        'model_count':model_count,
        'manuf_count':manuf_count,
        'date_count':date_count,
    })

def downloadcsv_view(request):
    report_file = get_report()
    return FileResponse(open(report_file, 'rb'))

def schedule_view(request, *args, **kwargs):
    schedule = get_schedule()
    return render(request, "schedule.html", {'schedule':schedule})

def stream_view(request, *args, **kwargs):
    stream_url = 'https://www.youtube.com/embed/7qXQ75fSd6s'
    if not request.user.is_authenticated:
        is_admin = False
    else:
        is_admin = request.user.is_superuser
    return render(request, "stream.html", {'stream_url':stream_url, 'is_admin':is_admin})