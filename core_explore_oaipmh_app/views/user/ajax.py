""" Ajax User core explore OAI-PMH
"""
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render
from core_explore_common_app.components.query.models import DataSource, Authentication
from core_oaipmh_harvester_app.components.oai_registry import api as oai_registry_api
import core_explore_common_app.components.query.api as api_query
import json


def get_data_source_list_oaipmh(request):
    """ Ajax method to fill the list of data sources.

    Args:
        request:

    Returns:

    """
    try:
        id_query = request.GET.get('id_query', None)

        if id_query is not None:
            # Get query from id
            query = api_query.get_by_id(id_query)
            instance_list = oai_registry_api.get_all_activated_registry(order_by_field='name')
            item_list = []
            url_instance = request.build_absolute_uri(reverse("core_explore_oaipmh_rest_execute_query"))
            for instance_item in instance_list:
                checked = False
                # compare instance with existing data source in query
                # in order to know if they have to be checked
                for data_source_item in query.data_sources:
                    if data_source_item.name == instance_item.name\
                       and data_source_item.url_query == url_instance:
                        checked = True
                        break

                # update the result item list for the context
                item_list.extend([{'instance_id': instance_item.id,
                                   'instance_name': instance_item.name,
                                   'is_checked': checked}])

            # Here, data sources are instances
            context_params = dict()
            context_params['instances'] = item_list

            # return context
            context = {}
            context.update(request)
            context.update(context_params)
            return render(request, 'core_explore_oaipmh_app/user/data_sources/list-content.html', context)
        else:
            return HttpResponseBadRequest("Error during loading data sources from oaipmh search.")
    except Exception as e:
        return HttpResponseBadRequest("Error during loading data sources from oaipmh search: %s" % e.message)


def update_data_source_list_oaipmh(request):
    """ Ajax method to update query data sources in data base.

    Args:
        request:

    Returns:

    """
    try:
        id_query = request.GET.get('id_query', None)
        id_instance = request.GET.get('id_instance', None)
        added = request.GET.get('to_be_added', None)
        to_be_added = json.loads(added) if added is not None else False

        # Get query from id
        if id_query is not None:
            query = api_query.get_by_id(id_query)
            url_instance = request.build_absolute_uri(reverse("core_explore_oaipmh_rest_execute_query"))
            instance = oai_registry_api.get_by_id(id_instance)
            if to_be_added:
                # Instance have to be added in the query as a data source
                authentication = Authentication(type='session')
                data_source = DataSource(name=instance.name, url_query=url_instance, authentication=authentication)
                data_source.query_options = {'instance_id': str(instance.id)}
                api_query.add_data_source(query, data_source)
            else:
                # Data source have to be remove from the query
                data_source = api_query.get_data_source_by_name_and_url_query(query, instance.name, url_instance)
                api_query.remove_data_source(query, data_source)

            return HttpResponse()
        else:
            return HttpResponseBadRequest("Error during data source selection.")
    except Exception as e:
        return HttpResponseBadRequest("Error during data source selection: %s" % e.message)
