from django.contrib import messages
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from exedev import notify, reflection

from . import systemd


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


SERVICE_COLUMNS = {
    'name': 'Name',
    'description': 'Description',
}

# Status groups in display order, and whether each starts expanded.
SERVICE_GROUPS = {
    systemd.Status.FAILED: True,
    systemd.Status.RUNNING: True,
    systemd.Status.SCHEDULED: True,
    systemd.Status.NOT_RUNNING: False,
}


def services(request: HttpRequest) -> HttpResponse:
    """Services grouped by status, each group sorted by ?sort=<column>, or ?sort=-<column> for descending."""
    sort = request.GET.get('sort', 'name')
    field = sort.removeprefix('-')
    if field not in SERVICE_COLUMNS:
        field, sort = 'name', 'name'
    descending = sort.startswith('-')

    columns = [
        {
            'title': title,
            'next_sort': f'-{key}' if key == field and not descending else key,
            'direction': ('desc' if descending else 'asc') if key == field else None,
        }
        for key, title in SERVICE_COLUMNS.items()
    ]
    services = sorted(
        systemd.get_services(),
        key=lambda s: getattr(s, field).lower(),
        reverse=descending,
    )
    groups = [
        {
            'status': status,
            'open': open_,
            'services': [s for s in services if s.status == status],
        }
        for status, open_ in SERVICE_GROUPS.items()
    ]
    # Nothing failing is the normal case, so don't show an empty Failed group.
    groups = [g for g in groups if g['services'] or g['status'] != systemd.Status.FAILED]
    return render(request, 'simple_exe_dev/services.html', {
        'columns': columns,
        'groups': groups,
    })


def service(request: HttpRequest, name: str) -> HttpResponse:
    service = systemd.get_service(name)
    if service is None:
        raise Http404(f'No service named {name}.')
    return render(request, 'simple_exe_dev/service.html', {'service': service})
