from django.apps import AppConfig


class Bio9Config(AppConfig):
    name = 'bIo9'

    def ready(self):
        import bIo9.notifications
