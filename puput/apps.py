from django.apps import AppConfig


class PuputAppConfig(AppConfig):
    name = 'puput'
    verbose_name = 'Puput'

    def ready(self):
        import puput.signals  # noqa: F401
