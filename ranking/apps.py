from django.apps import AppConfig


class RankingConfig(AppConfig):
    name = 'ranking'

    def ready(self):
        import ranking.signals