""" Settings for core_explore_oaipmh_app

Settings with the following syntax can be overwritten at the project level:
SETTING_NAME = getattr(settings, "SETTING_NAME", "Default Value")
"""
from django.conf import settings

if not settings.configured:
    settings.configure()

INSTALLED_APPS = getattr(settings, "INSTALLED_APPS", [])
