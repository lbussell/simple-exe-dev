from django.urls import path

from .views import index, integrations, notifications

urlpatterns = [
    path('', index, name='index'),
    path('notifications/', notifications, name='notifications'),
    path('integrations/', integrations, name='integrations'),
]
