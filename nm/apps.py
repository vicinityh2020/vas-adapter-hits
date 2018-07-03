from django.apps import AppConfig


class NmConfig(AppConfig):
    name = 'nm'

    def ready(self):
        # from nm.client import NMClient
        #
        # nm_client = NMClient()
        # nm_client.auth()
        pass
