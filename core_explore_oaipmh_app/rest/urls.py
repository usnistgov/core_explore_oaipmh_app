"""Url router for the REST API
"""
from django.conf.urls import url
from core_explore_oaipmh_app.rest.query import views as query_views

urlpatterns = [
    url(r'^execute-query$', query_views.execute_query,
        name='core_explore_oaipmh_rest_execute_query'),

]
