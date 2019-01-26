from django.apps import AppConfig


class StudentsConfig(AppConfig):
    name = 'students'

    def ready(self):
        # everytime server restarts
        import LibraryManagementSystem.signals
