from django.apps import AppConfig


class DidicloudConfig(AppConfig):
    name = 'didicloud'

    def ready(self):
        super().ready()
