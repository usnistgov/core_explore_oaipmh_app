"""Explore OAI-PMH user views
"""
from core_main_app.utils.rendering import render
from core_oaipmh_harvester_app.components.oai_record import api as oai_record_api
from core_main_app.utils.view_builders import data as data_view_builder


def data_detail(request):
    """Display data's detail for OAI-PMH

    Args:
        request:

    Returns:

    """
    try:
        record = oai_record_api.get_by_id(request.GET["id"])
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

        return data_view_builder.render_page(request, render, page_context)
    except Exception as e:
        error_message = "An error occured: {0}".format(str(e))
        return render(
            request,
            "core_main_app/common/commons/error.html",
            context={"error": error_message},
        )
