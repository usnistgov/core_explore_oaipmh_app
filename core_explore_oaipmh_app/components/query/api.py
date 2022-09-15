""" OaiPmh Query api
"""
import core_explore_common_app.components.query.api as api_query
from core_explore_common_app.access_control.api import can_access
from core_explore_common_app.components.query.api import upsert
from core_main_app.access_control.decorators import access_control


@access_control(can_access)
def add_oaipmh_data_source(query, data_source, user):
    """Add an oaipmh data source to the query

    Args:
        query:
        data_source:
        user:

    Returns:

    """
    # the unique identifier for an oaipmh data source is its instance_id
    # because there is no constraint on the name
    data_source_found = False
    for data_source_item in query.data_sources:
        if (
            "instance_id" in data_source_item["query_options"]
            and data_source_item["query_options"]["instance_id"]
            == data_source.query_options["instance_id"]
        ):
            data_source_found = True

    if not data_source_found:
        # add data source to query if not present
        query.data_sources.append(data_source)
        # update query
        return upsert(query, user)


@access_control(can_access)
def remove_oaipmh_data_source(query, instance_id, user):
    """Remove an oaipmh data source to the query

    Args:
        query:
        instance_id:

    Returns:

    """
    data_source = None
    for data_source_item in query.data_sources:
        if (
            "instance_id" in data_source_item["query_options"]
            and data_source_item["query_options"]["instance_id"] == instance_id
        ):
            data_source = data_source_item

    if data_source:
        return api_query.remove_data_source(query, data_source, user)
