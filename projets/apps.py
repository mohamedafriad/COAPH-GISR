from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProjetsConfig(AppConfig):
    name = 'projets'
    verbose_name = _('projets')
