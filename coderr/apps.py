from django.apps import AppConfig


class CoderrAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'coderr'

    # def ready(self):
    #     import coderr_app.signals  