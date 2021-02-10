
from django.contrib import admin
from django.urls import path, include
from pages.views import (
    home_view,
    login_view,
    lk_view,
    about_view,
    warehouse_view
)

from django.conf.urls import url


urlpatterns = [
    path('', home_view),    
    path('admin/', admin.site.urls),
    path('about/', about_view),
    path('warehouse/', warehouse_view), 
     url(r'^account/', include('accounts.urls')),

]
