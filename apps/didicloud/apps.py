from django.apps import AppConfig


class DidicloudConfig(AppConfig):
    name = 'didicloud'

    def ready(self):
        from . import signals_handler
        super().ready()
