from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "voter_influencer.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import voter_influencer.users.signals  # noqa F401
        except ImportError:
            pass
