from django.urls import path
from django.views.generic.base import RedirectView


app_name = 'websocket_connection'
urlpatterns = [
    path('index/', RedirectView.as_view(pattern_name='admin:login'), name='index'),
]