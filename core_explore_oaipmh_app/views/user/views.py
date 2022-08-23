"""Explore OAI-PMH user views
"""
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.utils.rendering import render
from core_main_app.utils.view_builders import data as data_view_builder
from core_oaipmh_harvester_app.components.oai_record import api as oai_record_api


def data_detail(request):
    """Display data's detail for OAI-PMH

    Args:
        request:

    Returns:

    """
    try:
        record = oai_record_api.get_by_id(request.GET["id"], request.user)
        template = record.harvester_metadata_format.template

        data_object = {
            "record_id": record.id,
            "title": record.identifier,
            "xml_content": record.xml_content,
            "template": {
                "id": template.id if template is not None else "",
                "display_name": record.harvester_metadata_format.get_display_name(),
                "hash": record.harvester_metadata_format.hash,
            },
        }

        page_context = data_view_builder.build_page(data_object)

        return data_view_builder.render_page(
            request, render, "core_main_app/user/data/detail.html", page_context
        )
    except AccessControlError:
        error_message = "Access Forbidden"
        status_code = 403
    except Exception as exception:
        error_message = f"An error occurred: {str(exception)}"
        status_code = 400
    return render(
        request,
        "core_main_app/common/commons/error.html",
        context={"error": error_message, "status_code": status_code},
    )
