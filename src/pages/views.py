from django.shortcuts import render
from django.http import HttpResponse


def home_view(request, *args, **kwargs):
    return render(request, "home.html", {})


def about_view(request, *args, **kwargs):
    return render(request, "about.html", {})


def reg_view(request, *args, **kwargs):
    return render(request, "reg.html", {})


def login_view(request, *args, **kwargs):
    return render(request, "login.html", {})


def lk_view(request, *args, **kwargs):
    return render(request, "lk.html", {})


def warehouse_view(request, *args, **kwargs):
    return render(request, "warehouse.html", {})