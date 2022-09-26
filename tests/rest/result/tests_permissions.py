""" Permissions Test for OAI Explore Result Rest API
"""
from django.test import SimpleTestCase
from unittest.mock import patch, Mock
from rest_framework import status

from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock
from core_oaipmh_harvester_app.components.oai_record import (
    api as oai_record_api,
)
from core_oaipmh_harvester_app.components.oai_record.models import OaiRecord
from core_explore_common_app.rest.result.serializers import ResultSerializer
from core_explore_oaipmh_app.rest.result import views as result_views


class TestGetResultQueryRegistry(SimpleTestCase):
    """Test Get Result Query Registry"""

    def setUp(self):
        """setUp"""
        super().setUp()
        self.data = {"id": 1}

    @patch.object(ResultSerializer, "data")
    @patch.object(oai_record_api, "get_by_id")
    def test_anonymous_returns_http_200(
        self, mock_oai_record_api_get_by_id, mock_serializer_data
    ):
        """test_anonymous_returns_http_200"""

        # Arrange
        mock_oai_record_api_get_by_id.return_value = Mock(spec=OaiRecord)
        mock_serializer_data.return_value = Mock(spec=ResultSerializer)

        # Act
        response = RequestMock.do_request_get(
            result_views.get_result_from_data_id, None, data=self.data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(ResultSerializer, "data")
    @patch.object(oai_record_api, "get_by_id")
    def test_authenticated_returns_http_200(
        self, mock_oai_record_api_get_by_id, mock_serializer_data
    ):
        """test_authenticated_returns_http_200"""

        # Arrange
        user = create_mock_user("1")
        mock_oai_record_api_get_by_id.return_value = Mock(spec=OaiRecord)
        mock_serializer_data.return_value = Mock(spec=ResultSerializer)

        # Act
        response = RequestMock.do_request_get(
            result_views.get_result_from_data_id, user=user, data=self.data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(ResultSerializer, "data")
    @patch.object(oai_record_api, "get_by_id")
    def test_staff_returns_http_200(
        self, mock_oai_record_api_get_by_id, mock_serializer_data
    ):
        """test_staff_returns_http_200"""

        # Arrange
        user = create_mock_user("1", is_staff=True)
        mock_oai_record_api_get_by_id.return_value = Mock(spec=OaiRecord)
        mock_serializer_data.return_value = Mock(spec=ResultSerializer)

        # Act
        response = RequestMock.do_request_get(
            result_views.get_result_from_data_id, user=user, data=self.data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
