""" Permissions Test for OAI Explore Query Rest API
"""
from django.test import SimpleTestCase
from mock.mock import patch
from rest_framework import status
from rest_framework.response import Response

from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock
from core_oaipmh_harvester_app.rest.oai_record.abstract_views import (
    AbstractExecuteQueryView,
)
from core_explore_oaipmh_app.rest.query import views as query_views


class TestGetExecuteQueryRegistry(SimpleTestCase):
    """Test Get Execute Query Registry"""

    def setUp(self):
        """setUp"""

        super().setUp()
        self.one_record_data = {
            "query": "{"
            '"experiment.experimentType.tracerDiffusivity.material.materialName": "Test 1"}'
        }
        self.user = create_mock_user("1")

    @patch.object(AbstractExecuteQueryView, "execute_query")
    def test_anonymous_returns_http_200(self, mock_execute_query):
        """test_anonymous_returns_http_200"""

        # Arrange
        data = self.one_record_data
        mock_execute_query.return_value = Response(status=status.HTTP_200_OK)

        # Act
        response = RequestMock.do_request_get(
            query_views.ExecuteQueryView.as_view(), None, data=data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(AbstractExecuteQueryView, "execute_query")
    def test_authenticated_returns_http_200(self, mock_execute_query):
        """test_authenticated_returns_http_200"""

        # Arrange
        user = create_mock_user("1")
        data = self.one_record_data
        mock_execute_query.return_value = Response(status=status.HTTP_200_OK)

        # Act
        response = RequestMock.do_request_get(
            query_views.ExecuteQueryView.as_view(), user=user, data=data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(AbstractExecuteQueryView, "execute_query")
    def test_staff_returns_http_200(self, mock_execute_query):
        """test_staff_returns_http_200"""

        # Arrange
        user = create_mock_user("1", is_staff=True)
        data = self.one_record_data
        mock_execute_query.return_value = Response(status=status.HTTP_200_OK)

        # Act
        response = RequestMock.do_request_get(
            query_views.ExecuteQueryView.as_view(), user=user, data=data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestPostExecuteQueryRegistry(SimpleTestCase):
    """Test Post Execute Query Registry"""

    def setUp(self):
        """setUp"""

        super().setUp()
        self.one_record_data = {
            "query": "{"
            '"experiment.experimentType.tracerDiffusivity.material.materialName": "Test 1"}'
        }
        self.user = create_mock_user("1")

    @patch.object(AbstractExecuteQueryView, "execute_query")
    def test_anonymous_returns_http_200(self, mock_execute_query):
        """test_anonymous_returns_http_200"""

        # Arrange
        data = self.one_record_data
        mock_execute_query.return_value = Response(status=status.HTTP_200_OK)

        # Act
        response = RequestMock.do_request_post(
            query_views.ExecuteQueryView.as_view(), None, data=data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(AbstractExecuteQueryView, "execute_query")
    def test_authenticated_returns_http_200(self, mock_execute_query):
        """test_authenticated_returns_http_200"""

        # Arrange
        user = create_mock_user("1")
        data = self.one_record_data
        mock_execute_query.return_value = Response(status=status.HTTP_200_OK)

        # Act
        response = RequestMock.do_request_post(
            query_views.ExecuteQueryView.as_view(), user=user, data=data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(AbstractExecuteQueryView, "execute_query")
    def test_staff_returns_http_200(self, mock_execute_query):
        """test_staff_returns_http_200"""

        # Arrange
        user = create_mock_user("1", is_staff=True)
        data = self.one_record_data
        mock_execute_query.return_value = Response(status=status.HTTP_200_OK)

        # Act
        response = RequestMock.do_request_post(
            query_views.ExecuteQueryView.as_view(), user=user, data=data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
