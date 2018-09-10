from django.urls import path
from django.views.generic.base import RedirectView


app_name = 'shallow'
urlpatterns = [
    path('index/', RedirectView.as_view(pattern_name='admin:login'), name='index'),
]