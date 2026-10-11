from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from exedev import notify, reflection


def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'simple_exe_dev/index.html', {
        'info': reflection.get_info(),
        'email': reflection.get_email(),
        'tags': reflection.get_tags(),
        'comment': reflection.get_comment(),
        'default_port': reflection.get_default_port(),
        'integrations': reflection.get_integrations(),
    })


@require_POST
def send_notification(request: HttpRequest) -> HttpResponse:
    notify.send(request.POST['title'], request.POST['body'])
    messages.success(request, 'Notification sent.')
    return redirect('index')
