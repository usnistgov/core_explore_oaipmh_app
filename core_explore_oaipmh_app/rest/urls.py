"""Url router for the REST API
"""

from django.urls import re_path

from core_explore_oaipmh_app.rest.query import views as query_views
from core_explore_oaipmh_app.rest.result import views as result_views

urlpatterns = [
    re_path(
        r"^execute-query",
        query_views.ExecuteQueryView.as_view(),
        name="core_explore_oaipmh_rest_execute_query",
    ),
    re_path(
        r"^result",
        result_views.get_result_from_data_id,
        name="core_explore_oaipmh_app_rest_get_result_from_data_id",
    ),
]
