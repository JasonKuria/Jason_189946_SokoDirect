from django.apps import AppConfig

class UsersConfig(AppConfig):
    name = 'users'

    # this method is called when the app is ready,
    # we will use it to import the signals and connect them
    
    def ready(self):
        import users.signals # import the signals to connect them when the app is ready

