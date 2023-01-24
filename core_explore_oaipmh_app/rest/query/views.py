""" REST views for the explore OAI-PMH API
"""

import json

import pytz
from django.conf import settings as conf_settings
from django.urls import reverse

import core_oaipmh_harvester_app.components.oai_record.api as oai_record_api
from core_explore_common_app.components.result.models import Result
from core_explore_common_app.rest.result.serializers import ResultSerializer
from core_main_app.commons.constants import DATA_JSON_FIELD
from core_main_app.commons.exceptions import ApiError
from core_main_app.settings import RESULTS_PER_PAGE
from core_main_app.utils.pagination.django_paginator.results_paginator import (
    ResultsPaginator,
)
from core_main_app.utils.pagination.mongoengine_paginator.paginator import (
    MongoenginePaginator,
)
from core_main_app.utils.pagination.rest_framework_paginator.pagination import (
    StandardResultsSetPagination,
)
from core_oaipmh_harvester_app.components.oai_harvester_metadata_format import (
    api as oai_harvester_metadata_format_api,
)
from core_oaipmh_harvester_app.components.oai_registry import (
    api as oai_registry_api,
)
from core_oaipmh_harvester_app.rest.oai_record.abstract_views import (
    AbstractExecuteQueryView,
)
from core_oaipmh_harvester_app.utils.query.mongo.query_builder import (
    OaiPmhQueryBuilder,
)


# TODO: check if keeping this one is useful, only used in PID (may be able to do local call too)
class ExecuteQueryView(AbstractExecuteQueryView):
    """Execute Query View"""

    def get_registries(self):
        """Get a list of registry ids. Should return empty list if not found. JSON format.

        Returns:
            List of registry ids (JSON format).

        """
        registries = []
        options = self.request.data.get("options", None)
        if options is not None:
            if (
                type(options) is str
            ):  # Try parsing options only if it is a string
                options = json.loads(options)

            registries.append(int(options["instance_id"]))

        return json.dumps(registries)

    def build_response(self, data_list):
        """Build the paginated response.

        Args:
            data_list: List of data.

        Returns:
            The response.

        """
        # Paginator
        paginator = StandardResultsSetPagination()
        # get requested page from list of results
        page = paginator.paginate_queryset(data_list, self.request)

        # Serialize object
        results = []
        url = reverse("core_explore_oaipmh_app_data_detail")
        url_access_data = reverse(
            "core_explore_oaipmh_app_rest_get_result_from_data_id"
        )
        # Template info
        template_info = dict()
        for data in page:
            # get data's metadata format
            metadata_format = data.harvester_metadata_format
            # get and store data's template information from metadata format
            if metadata_format not in template_info:
                template = data.harvester_metadata_format.template
                template_info[
                    metadata_format
                ] = get_template_info_from_metadata_format_and_template(
                    metadata_format, template
                )

            results.append(
                Result(
                    title=data.title,
                    xml_content=data.xml_content,
                    template_info=template_info[metadata_format],
                    permission_url=None,
                    detail_url=f"{url}?id={str(data.id)}",
                    last_modification_date=data.last_modification_date.replace(
                        tzinfo=pytz.UTC
                    ),
                    access_data_url=f"{url_access_data}?id={str(data.id)}",
                )
            )

        # Serialize results
        serialized_results = ResultSerializer(results, many=True)
        # Return http response
        return paginator.get_paginated_response(serialized_results.data)


def get_template_info_from_metadata_format_and_template(
    harvester_metadata_format, template
):
    """Get template information from metadata format and template
    Args:
        harvester_metadata_format: Metadata format
        template: Related template

    Returns:
        Template information.

    """
    # Use the metadata prefix name
    name = harvester_metadata_format.get_display_name()

    # Here the id need to be set anyway because is expected by the serializer
    return_value = {
        "id": template.id if template is not None else "",
        "name": name,
        "hash": harvester_metadata_format.hash,
    }

    return return_value


def get_registries(data):
    """Get a list of registry ids. Should return empty list if not found. JSON format.

    Returns:
        List of registry ids (JSON format).

    """
    registries_list = []
    options = data.get("options", None)
    if options is not None:
        if type(options) is str:  # Try parsing options only if it is a string
            options = json.loads(options)

        registries_list.append(int(options["instance_id"]))

    return json.dumps(registries_list)


def execute_oaipmh_query(query_data, page, request):
    """Execute query on OAI-PMH database

    Args:
        query_data:
        page:
        request:

    Returns:

    """
    # get query and templates
    query = query_data.get("query", None)
    templates = query_data.get("templates", "[]")
    registries = get_registries(query_data)
    order_by_field = query_data.get("order_by_field", None)

    if order_by_field:
        order_by_field = order_by_field.split(",")

    if query is None:
        raise ApiError("Query should be passed in parameter.")

    # build query builder
    query_builder = OaiPmhQueryBuilder(query, DATA_JSON_FIELD)

    if type(templates) is str:
        templates = json.loads(templates)

    if type(registries) is str:
        registries = json.loads(registries)

    # if registries, check if activated
    list_activated_registry = list(
        oai_registry_api.get_all_activated_registry().values_list(
            "id", flat=True
        )
    )
    if len(registries) > 0:
        activated_registries = [
            activated_registry_id
            for activated_registry_id in registries
            if activated_registry_id in list_activated_registry
        ]
    else:
        activated_registries = list_activated_registry

    if len(templates) > 0:
        # get list of template ids
        list_template_ids = [template["id"] for template in templates]
        # get all metadata formats used by the registries
        list_metadata_format = (
            oai_harvester_metadata_format_api.get_all_by_list_registry_ids(
                activated_registries
            )
        )
        # Filter metadata formats that use the given templates
        list_metadata_formats_id = [
            str(x.id)
            for x in list_metadata_format
            if x.template is not None
            and str(x.template.id) in list_template_ids
        ]
        query_builder.add_list_metadata_formats_criteria(
            list_metadata_formats_id
        )
    else:
        # Only activated registries
        query_builder.add_list_registries_criteria(activated_registries)

    # do not include deleted records
    query_builder.add_not_deleted_criteria()
    # create a raw query
    raw_query = query_builder.get_raw_query()
    # execute query
    data_list = oai_record_api.execute_json_query(
        raw_query, request.user, order_by_field
    )
    # build result page
    if conf_settings.MONGODB_INDEXING:
        paginator = MongoenginePaginator(data_list, RESULTS_PER_PAGE)
        page = paginator.get_page(page)
    else:
        paginator = ResultsPaginator()
        page = paginator.get_results(data_list, page, RESULTS_PER_PAGE)
    return page


def format_oaipmh_results(results, request):
    """Format local results for explore apps

    Args:
        results:
        request:

    Returns:

    """
    url = reverse("core_explore_oaipmh_app_data_detail")
    url_access_data = reverse(
        "core_explore_oaipmh_app_rest_get_result_from_data_id"
    )
    # Template info
    template_info = dict()
    # Init data list
    data_list = []
    for data in results.object_list:
        # get data's metadata format
        metadata_format = data.harvester_metadata_format
        # get and store data's template information from metadata format
        if metadata_format not in template_info:
            template = data.harvester_metadata_format.template
            template_info[
                metadata_format
            ] = get_template_info_from_metadata_format_and_template(
                metadata_format, template
            )

        data_list.append(
            Result(
                title=data.title,
                xml_content=data.xml_content,
                template_info=template_info[metadata_format],
                permission_url=None,
                detail_url=f"{url}?id={str(data.id)}",
                last_modification_date=data.last_modification_date.replace(
                    tzinfo=pytz.UTC
                ),
                access_data_url=f"{url_access_data}?id={str(data.id)}",
            )
        )
    return data_list
