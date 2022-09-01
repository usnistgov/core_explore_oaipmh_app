""" REST views for the explore OAI-PMH API
"""
import json

import pytz
from django.urls import reverse

from core_explore_common_app.components.result.models import Result
from core_explore_common_app.rest.result.serializers import ResultSerializer
from core_main_app.utils.pagination.rest_framework_paginator.pagination import (
    StandardResultsSetPagination,
)
from core_oaipmh_harvester_app.rest.oai_record.abstract_views import (
    AbstractExecuteQueryView,
)


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
            if type(options) is str:  # Try parsing options only if it is a string
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
