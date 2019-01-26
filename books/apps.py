from django.apps import AppConfig


class BooksConfig(AppConfig):
    name = 'books'

    def ready(self):
        import LibraryManagementSystem.signals
