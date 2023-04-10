""" Ajax User core explore OAI-PMH
"""
import json

from django.http import HttpResponseForbidden
from django.http.response import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render
from django.utils.html import escape

import core_explore_common_app.components.query.api as api_query
from core_explore_common_app.components.abstract_query.models import (
    Authentication,
    DataSource,
)
from core_explore_oaipmh_app.components.query import api as oaipmh_query_api
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.settings import DATA_SORTING_FIELDS, SERVER_URI
from core_main_app.templatetags.xsl_transform_tag import (
    render_xml_as_html_detail,
)
from core_oaipmh_harvester_app.components.oai_record import (
    api as oai_record_api,
)
from core_oaipmh_harvester_app.components.oai_registry import (
    api as oai_registry_api,
)


def get_data_source_list_oaipmh(request):
    """Ajax method to fill the list of data sources.

    Args:
        request:

    Returns:

    """
    try:
        id_query = request.GET.get("id_query", None)

        if id_query is None:
            return HttpResponseBadRequest(
                "Error during loading data sources from oaipmh search."
            )

        # Get query from id
        query = api_query.get_by_id(id_query, request.user)
        instance_list = oai_registry_api.get_all_activated_registry(
            order_by_field="name"
        )
        item_list = []
        for instance_item in instance_list:
            checked = False
            # compare instance with existing data source in query
            # in order to know if they have to be checked
            for data_source_item in query.data_sources:
                if "instance_id" in data_source_item[
                    "query_options"
                ] and data_source_item["query_options"]["instance_id"] == str(
                    instance_item.id
                ):
                    checked = True

            # update the result item list for the context
            item_list.extend(
                [
                    {
                        "instance_id": instance_item.id,
                        "instance_name": instance_item.name,
                        "is_checked": checked,
                    }
                ]
            )

        # Here, data sources are instances
        context_params = dict()
        context_params["instances"] = item_list

        # return context
        context = {}
        context.update(request)
        context.update(context_params)
        return render(
            request,
            "core_explore_oaipmh_app/user/data_sources/list-content.html",
            context,
        )

    except AccessControlError:
        return HttpResponseForbidden()
    except Exception as exception:
        return HttpResponseBadRequest(
            f"Error during loading data sources from oaipmh search: {escape(str(exception))}"
        )


def update_data_source_list_oaipmh(request):
    """Ajax method to update query data sources in data base.

    Args:
        request:

    Returns:

    """
    try:
        id_query = request.GET.get("id_query", None)
        id_instance = request.GET.get("id_instance", None)
        added = request.GET.get("to_be_added", None)
        to_be_added = json.loads(added) if added is not None else False

        # Get query from id
        if id_query is None:
            return HttpResponseBadRequest(
                "Error during data source selection."
            )

        query = api_query.get_by_id(id_query, request.user)
        instance = oai_registry_api.get_by_id(id_instance)
        if to_be_added:
            # Instance have to be added in the query as a data source
            authentication = Authentication(auth_type="session")
            data_source = DataSource(
                name=instance.name,
                url_query=SERVER_URI,
                authentication=authentication,
                order_by_field=",".join(DATA_SORTING_FIELDS),
                query_options={"instance_id": str(instance.id)},
            )

            oaipmh_query_api.add_oaipmh_data_source(
                query, data_source, request.user
            )
        else:
            oaipmh_query_api.remove_oaipmh_data_source(
                query, id_instance, request.user
            )

        return HttpResponse()

    except AccessControlError:
        return HttpResponseForbidden()
    except Exception as exception:
        return HttpResponseBadRequest(
            f"Error during data source selection: {escape(str(exception))}"
        )


def change_data_display(request):
    """Change data display

    Args:
        request:

    Returns:
    """
    try:
        # get xslt id
        xsl_transformation_id = request.POST.get("xslt_id", None)
        # get oai_record
        record = oai_record_api.get_by_id(
            request.POST.get("data_id"), request.user
        )
        # get template id
        template_id = record.harvester_metadata_format.template.id
        # get template hash
        template_hash = record.harvester_metadata_format.template.hash
        # get xml content
        xml_content = record.xml_content

        # return content transformed
        return HttpResponse(
            json.dumps(
                {
                    "template": render_xml_as_html_detail(
                        xml_content=xml_content,
                        template_id=template_id,
                        template_hash=template_hash,
                        xslt_id=xsl_transformation_id,
                        request=request,
                    ),
                }
            ),
            "application/javascript",
        )
    except AccessControlError:
        return HttpResponseForbidden("Access Forbidden")
    except Exception:
        return HttpResponseBadRequest("Unexpected error")
