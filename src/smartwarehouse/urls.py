
from django.contrib import admin
from django.urls import path, include
from pages.views import (
    home_view,
    about_view,
    warehouse_view,
    stream_view,
    schedule_view
)

from django.conf.urls import url


urlpatterns = [
    path('', home_view, name='home'),    
    path('admin/', admin.site.urls, name='admin'),
    path('about/', about_view, name='about'),
    path('stream', stream_view, name='stream'),
    path('warehouse/', warehouse_view, name='warehouse'), 
    path('schedule/', schedule_view, name='schedule'), 
     url(r'^account/', include('accounts.urls')),

]
