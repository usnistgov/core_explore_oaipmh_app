""" Url router for the explore OAI-PMH search application
"""
from django.conf.urls import url, include
import core_explore_oaipmh_app.views.user.views as user_views
import core_explore_oaipmh_app.views.user.ajax as user_ajax


urlpatterns = [
    url(r'^get_data_sources', user_ajax.get_data_source_list_oaipmh,
        name='core_explore_oaipmh_app_get_data_sources'),
    url(r'^update_data_sources', user_ajax.update_data_source_list_oaipmh,
        name='core_explore_oaipmh_app_update_data_sources'),
    url(r'^data', user_views.data_detail,
        name='core_explore_oaipmh_app_data_detail'),
    url(r'^rest/', include('core_explore_oaipmh_app.rest.urls')),
]
