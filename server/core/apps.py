from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        # Automatically import all receivers files
        autodiscover_modules('receivers')
