""" Url router for the explore OAI-PMH search application
"""
from django.conf.urls import include
from django.contrib import admin
from django.urls import re_path

admin.autodiscover()


urlpatterns = [
    re_path(r"^", include("core_main_app.urls")),
    re_path(r"^", include("core_explore_oaipmh_app.urls")),
]
