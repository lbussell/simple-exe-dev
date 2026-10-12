from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from exedev import notify, reflection


def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'simple_exe_dev/index.html', {
        'info': reflection.get_info(),
        'email': reflection.get_email(),
        'tags': reflection.get_tags(),
        'comment': reflection.get_comment(),
        'default_port': reflection.get_default_port(),
    })


def notifications(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        notify.send(request.POST['title'], request.POST['body'])
        messages.success(request, 'Notification sent.')
        return redirect('notifications')
    return render(request, 'simple_exe_dev/notifications.html')


def integrations(request: HttpRequest) -> HttpResponse:
    return render(request, 'simple_exe_dev/integrations.html', {
        'integrations': reflection.get_integrations(),
    })
