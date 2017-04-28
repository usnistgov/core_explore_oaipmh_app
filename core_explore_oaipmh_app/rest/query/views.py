""" REST views for the explore OAI-PMH  API
"""
from core_oaipmh_common_app.commons.messages import OaiPmhMessage
from django.core.urlresolvers import reverse
from core_explore_common_app.components.result.models import Result
from core_explore_common_app.rest.result.serializers import ResultSerializer
from core_explore_oaipmh_app.utils.query.mongo.query_builder import OaiPmhQueryBuilder
from core_oaipmh_harvester_app.components.oai_harvester_metadata_format import api as oai_harvester_metadata_format_api
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from core_main_app.components.version_manager import api as version_manager_api
from core_main_app.utils.xml import unparse
import core_oaipmh_harvester_app.components.oai_record.api as oai_record_api
import json


@api_view(['POST'])
def execute_query(request):
    """ Executes query and returns results.

    Args:
        request: Request.

    Returns:
        Response: Response.

    """
    try:
        # get query
        query = request.POST.get('query', None)
        options = request.POST.get('options', None)

        if query is not None:
            query_builder = OaiPmhQueryBuilder(query, 'metadata')
        else:
            return Response('Query should be passed in parameter', status=status.HTTP_400_BAD_REQUEST)

        if options is not None:
            json_options = json.loads(options)
            instance_id = json_options['instance_id']
        else:
            return Response('Missing instance information.', status=status.HTTP_400_BAD_REQUEST)

        # update the content query with given templates
        if 'templates' in request.POST:
            templates = json.loads(request.POST['templates'])
            if len(templates) > 0:
                # get list of template ids
                list_template_ids = [template['id'] for template in templates]
                # get all metadata formats used by the instance (registry)
                list_metadata_format = oai_harvester_metadata_format_api.get_all_by_registry_id(instance_id)
                # Filter metadata formats that use the given templates
                list_metadata_formats_id = [str(x.id) for x in list_metadata_format
                                            if x.template is not None and str(x.template.id) in list_template_ids]
                query_builder.add_list_metadata_formats_criteria(list_metadata_formats_id)

        # create a raw query
        raw_query = query_builder.get_raw_query()
        # execute query
        data_list = oai_record_api.execute_query(raw_query)
        # Serialize object
        results = []
        url = reverse("core_explore_oaipmh_app_data_detail")
        # Template info
        template_info = dict()
        for data in data_list:
            # get data's template
            template = data.harvester_metadata_format.template
            # get and store data's template information (title, version)
            if template not in template_info:
                version_manager = version_manager_api.get_from_version(data.harvester_metadata_format.template)
                version_number = version_manager_api.get_version_number(version_manager,
                                                                        data.harvester_metadata_format.template.id)
                template_info[template] = {'title': version_manager.title, 'version': version_number}

            results.append(Result(title=data.identifier,
                                  xml_content=unparse(data.metadata),
                                  origin="{0} (version {1})".format(template_info[template].get('title'),
                                                                    template_info[template].get('version')),
                                  detail_url="{0}?id={1}".format(url, data.id)))

        return_value = ResultSerializer(results, many=True)

        return Response(return_value.data, status=status.HTTP_200_OK)
    except Exception as e:
        content = OaiPmhMessage.get_message_labelled('An error occurred when attempting to execute the query: %s'
                                                     % e.message)
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
