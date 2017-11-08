""" Apps file for setting core package when app is ready
"""
from core_main_app.utils.databases.pymongo_database import init_text_index
from django.apps import AppConfig


class ExploreOaiPmhAppConfig(AppConfig):
    """ Core application settings
    """
    name = 'core_explore_oaipmh_app'

    def ready(self):
        """ Run when the app is ready.

        Returns:

        """
        init_text_index('oai_record')
