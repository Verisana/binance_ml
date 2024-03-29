from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.views.generic.base import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(pattern_name='admin:login')),
    path('profiles/', include('profiles.urls')),
]

admin.site.site_header = 'Machine Learning Database'