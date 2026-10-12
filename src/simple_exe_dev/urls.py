from django.urls import path

from .views import index, integrations, notifications, service, services

urlpatterns = [
    path('', index, name='index'),
    path('notifications/', notifications, name='notifications'),
    path('integrations/', integrations, name='integrations'),
    path('services/', services, name='services'),
    path('services/<str:name>/', service, name='service'),
]
