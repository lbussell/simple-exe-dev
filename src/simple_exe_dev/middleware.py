from django.http import HttpRequest

from exedev import login

from .models import User


def exe_dev_user(get_response):
    """Set request.user from exe.dev login, creating the User on first sight.

    request.user is None when the request didn't come through exe.dev login.
    """

    def middleware(request: HttpRequest):
        request.user = None
        identity = login.get_identity(request.headers)
        if identity:
            user, created = User.objects.get_or_create(exe_id=identity.user_id, defaults={'email': identity.email})
            if not created and user.email != identity.email:
                user.email = identity.email
                user.save(update_fields=['email'])
            request.user = user
        return get_response(request)

    return middleware
