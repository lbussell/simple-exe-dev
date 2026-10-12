from django.db import models


class User(models.Model):
    """Someone signed in through exe.dev: https://exe.dev/docs/login-with-exe.md"""

    exe_id = models.CharField(max_length=255, unique=True)
    email = models.EmailField()
    display_name = models.CharField(max_length=100, blank=True)

    def __str__(self) -> str:
        return self.name

    @property
    def default_name(self) -> str:
        return self.email.partition('@')[0]

    @property
    def name(self) -> str:
        return self.display_name or self.default_name
