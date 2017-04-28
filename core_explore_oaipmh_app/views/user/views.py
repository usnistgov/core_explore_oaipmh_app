"""Explore OAI-PMH user views
"""
from core_main_app.utils.rendering import render
from core_oaipmh_harvester_app.components.oai_record import api as oai_record_api
from core_main_app.utils.xml import unparse


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
        data = {'title': record.identifier, 'xml_file': unparse(record.metadata)}
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
