"""Explore OAI-PMH user views
"""
from core_main_app.utils.rendering import render
from core_oaipmh_harvester_app.components.oai_record import api as oai_record_api


def data_detail(request):
    """ Display data's detail for OAI-PMH

    Args:
        request:

    Returns:

    """
    record_id = request.GET['id']
    data = dict()

    try:
        record = oai_record_api.get_by_id(record_id)
        template = record.harvester_metadata_format.template

        data = {'title': record.identifier, 'xml_content': record.xml_content,
                'template': {'id': template.id if template is not None else '',
                             'display_name': record.harvester_metadata_format.get_display_name(),
                             'hash': record.harvester_metadata_format.hash}}
    except:
        # TODO: catch good exception, redirect to error page
        pass

    context = {
        'data': data
    }

    assets = {
        "js": [
            {
                "path": 'core_main_app/common/js/XMLTree.js',
                "is_raw": False
            },
            {
                "path": 'core_main_app/user/js/data/detail.js',
                "is_raw": False
            },
        ],
        "css": ["core_main_app/common/css/XMLTree.css"],
    }

    return render(request, 'core_main_app/user/data/detail.html', context=context, assets=assets)
