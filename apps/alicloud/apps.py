from django.apps import AppConfig


class AlicloudConfig(AppConfig):
    name = 'alicloud'

    def ready(self):
        from . import signals_handler
        super().ready()
