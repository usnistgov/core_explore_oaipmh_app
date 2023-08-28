""" REST views for the data API
"""

from rest_framework import status
from rest_framework.decorators import api_view, schema
from rest_framework.response import Response

from core_explore_common_app.components.result.models import Result
from core_explore_common_app.rest.result.serializers import ResultSerializer
from core_main_app.commons.exceptions import DoesNotExist
from core_oaipmh_harvester_app.components.oai_record import (
    api as oai_record_api,
)


@api_view(["GET"])
@schema(None)
def get_result_from_data_id(request):
    """Access data, Returns Result, Expects a data ID

    Args:
        request:

    Returns:

    """
    try:
        # get parameters
        data_id = request.GET.get("id", None)
        # if no data id given
        if data_id is None:
            content = {"message": "Data id is missing"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        # reverse url for accessing data
        record = oai_record_api.get_by_id(data_id, request.user)
        # No title for OaiRecord. Use of the id.
        result = Result(title=str(data_id), content=record.content)
        # Serialize results
        return_value = ResultSerializer(result)
        # Returns the response
        return Response(return_value.data, status=status.HTTP_200_OK)
    except DoesNotExist:
        # The record doesn't exist with this id
        content = {"message": "No Record found with the given id."}
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    except Exception as exception:
        # if something went wrong, return an internal server error
        content = {"message": str(exception)}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
