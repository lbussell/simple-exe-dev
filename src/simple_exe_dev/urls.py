from django.urls import path

from .views import index, send_notification

urlpatterns = [
    path('', index, name='index'),
    path('notify/', send_notification, name='send_notification'),
]
