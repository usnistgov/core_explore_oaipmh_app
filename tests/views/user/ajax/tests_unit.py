""" Test user-side AJAX views
"""
from unittest import TestCase
from unittest.mock import patch, MagicMock

from django.test import RequestFactory
from rest_framework import status

from core_explore_oaipmh_app.views.user.ajax import (
    update_data_source_list_oaipmh,
)
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.settings import DATA_SORTING_FIELDS
from core_main_app.utils.tests_tools.MockUser import create_mock_user


class TestUpdateDataSourceListOaipmh(TestCase):
    """Test update_data_source_list_oaipmh function"""

    def setUp(self):
        """setUp"""
        self.factory = RequestFactory()
        self.view = "core_explore_oaipmh_app_update_data_sources"
        self.user = create_mock_user(user_id="1")

    def _send_request(self, data: dict = None):
        """_send_request"""
        request = self.factory.get(self.view)
        request.user = self.user
        request.GET = {} if not data else data

        return update_data_source_list_oaipmh(request)

    def test_id_query_none_returns_400(self):
        """test_id_query_none_returns_400"""
        self.assertEquals(
            self._send_request().status_code, status.HTTP_400_BAD_REQUEST
        )

    @patch("core_explore_oaipmh_app.views.user.ajax.api_query.get_by_id")
    def test_query_get_by_id_fails_returns_400(self, mock_query_get_by_id):
        """test_query_get_by_id_fails_returns_400"""
        mock_query_get_by_id.side_effect = Exception(
            "mock_query_get_by_id_exception"
        )
        self.assertEquals(
            self._send_request({"id_query": "mock_id_query"}).status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    @patch("core_explore_oaipmh_app.views.user.ajax.api_query.get_by_id")
    def test_query_get_by_id_acl_error_returns_403(self, mock_query_get_by_id):
        """test_query_get_by_id_acl_error_returns_403"""
        mock_query_get_by_id.side_effect = AccessControlError(
            "mock_query_get_by_id_exception"
        )
        self.assertEquals(
            self._send_request({"id_query": "mock_id_query"}).status_code,
            status.HTTP_403_FORBIDDEN,
        )

    @patch("django.http.HttpRequest.build_absolute_uri")
    @patch("core_explore_oaipmh_app.views.user.ajax.api_query.get_by_id")
    def test_build_absolute_uri_fails_returns_400(
        self, mock_query_get_by_id, mock_build_absolute_uri
    ):
        """test_build_absolute_uri_fails_returns_400"""
        mock_query_get_by_id.return_value = "mock_query"
        mock_build_absolute_uri.side_effect = Exception(
            "mock_build_absolute_uri_exception"
        )
        self.assertEquals(
            self._send_request({"id_query": "mock_id_query"}).status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    @patch(
        "core_explore_oaipmh_app.views.user.ajax.oai_registry_api.get_by_id"
    )
    @patch("django.http.HttpRequest.build_absolute_uri")
    @patch("core_explore_oaipmh_app.views.user.ajax.api_query.get_by_id")
    def test_registry_get_by_id_fails_returns_400(
        self,
        mock_query_get_by_id,
        mock_build_absolute_uri,
        mock_oai_registry_get_by_id,
    ):
        """test_registry_get_by_id_fails_returns_400"""
        mock_query_get_by_id.return_value = "mock_query"
        mock_build_absolute_uri.return_value = "mock_url_instance"
        mock_oai_registry_get_by_id.side_effect = Exception(
            "mock_oai_registry_get_by_id"
        )
        self.assertEquals(
            self._send_request({"id_query": "mock_id_query"}).status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    @patch(
        "core_explore_oaipmh_app.views.user.ajax.oaipmh_query_api.add_oaipmh_data_source"
    )
    @patch(
        "core_explore_oaipmh_app.views.user.ajax.oai_registry_api.get_by_id"
    )
    @patch("django.http.HttpRequest.build_absolute_uri")
    @patch("core_explore_oaipmh_app.views.user.ajax.api_query.get_by_id")
    def test_data_source_capabilities_added_when_linked_records_installed(
        self,
        mock_query_get_by_id,
        mock_build_absolute_uri,
        mock_oai_registry_get_by_id,
        mock_add_oaipmh_data_source,
    ):
        """test_data_source_capabilities_added_when_linked_records_installed"""
        mock_oai_registry = MagicMock()
        mock_url_instance = "mock_url_instance"
        mock_query_get_by_id.return_value = "mock_query"
        mock_build_absolute_uri.return_value = mock_url_instance
        mock_oai_registry_get_by_id.return_value = mock_oai_registry

        self._send_request(
            {"id_query": "mock_id_query", "to_be_added": "true"}
        )
        mock_add_oaipmh_data_source.assert_called_with(
            "mock_query",
            {
                "name": mock_oai_registry.name,
                "url_query": mock_url_instance,
                "authentication": {"auth_type": "session", "params": {}},
                "order_by_field": ",".join(DATA_SORTING_FIELDS),
                "query_options": {"instance_id": str(mock_oai_registry.id)},
                "capabilities": {"url_pid": "mock_url_instance"},
            },
            self.user,
        )

    @patch("core_explore_oaipmh_app.views.user.ajax.settings.INSTALLED_APPS")
    @patch(
        "core_explore_oaipmh_app.views.user.ajax.oaipmh_query_api.add_oaipmh_data_source"
    )
    @patch(
        "core_explore_oaipmh_app.views.user.ajax.oai_registry_api.get_by_id"
    )
    @patch("django.http.HttpRequest.build_absolute_uri")
    @patch("core_explore_oaipmh_app.views.user.ajax.api_query.get_by_id")
    def test_data_source_capabilities_empty_when_linked_records_not_installed(
        self,
        mock_query_get_by_id,
        mock_build_absolute_uri,
        mock_oai_registry_get_by_id,
        mock_add_oaipmh_data_source,
        mock_installed_apps,
    ):
        """test_data_source_capabilities_empty_when_linked_records_not_installed"""
        mock_oai_registry = MagicMock()
        mock_url_instance = "mock_url_instance"
        mock_query_get_by_id.return_value = "mock_query"
        mock_build_absolute_uri.return_value = mock_url_instance
        mock_oai_registry_get_by_id.return_value = mock_oai_registry
        mock_installed_apps.return_value = []

        self._send_request(
            {"id_query": "mock_id_query", "to_be_added": "true"}
        )
        mock_add_oaipmh_data_source.assert_called_with(
            "mock_query",
            {
                "name": mock_oai_registry.name,
                "url_query": mock_url_instance,
                "authentication": {"auth_type": "session", "params": {}},
                "order_by_field": ",".join(DATA_SORTING_FIELDS),
                "query_options": {"instance_id": str(mock_oai_registry.id)},
                "capabilities": {},
            },
            self.user,
        )

    @patch(
        "core_explore_oaipmh_app.views.user.ajax.oaipmh_query_api.add_oaipmh_data_source"
    )
    @patch(
        "core_explore_oaipmh_app.views.user.ajax.oai_registry_api.get_by_id"
    )
    @patch("django.http.HttpRequest.build_absolute_uri")
    @patch("core_explore_oaipmh_app.views.user.ajax.api_query.get_by_id")
    def test_add_oaipmh_data_source_fails_returns_400(
        self,
        mock_query_get_by_id,
        mock_build_absolute_uri,
        mock_oai_registry_get_by_id,
        mock_add_oaipmh_data_source,
    ):
        """test_add_oaipmh_data_source_fails_returns_400"""
        mock_oai_registry = MagicMock()
        mock_url_instance = "mock_url_instance"
        mock_query_get_by_id.return_value = "mock_query"
        mock_build_absolute_uri.return_value = mock_url_instance
        mock_oai_registry_get_by_id.return_value = mock_oai_registry
        mock_add_oaipmh_data_source.side_effect = Exception(
            "mock_add_oaipmh_data_source_exception"
        )

        self.assertEquals(
            self._send_request(
                {"id_query": "mock_id_query", "to_be_added": "true"}
            ).status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    @patch(
        "core_explore_oaipmh_app.views.user.ajax.oaipmh_query_api.remove_oaipmh_data_source"
    )
    @patch(
        "core_explore_oaipmh_app.views.user.ajax.oai_registry_api.get_by_id"
    )
    @patch("django.http.HttpRequest.build_absolute_uri")
    @patch("core_explore_oaipmh_app.views.user.ajax.api_query.get_by_id")
    def test_remove_oaipmh_data_source_called_when_not_to_be_added(
        self,
        mock_query_get_by_id,
        mock_build_absolute_uri,
        mock_oai_registry_get_by_id,
        mock_remove_oaipmh_data_source,
    ):
        """test_remove_oaipmh_data_source_called_when_not_to_be_added"""
        mock_oai_registry = MagicMock()
        mock_url_instance = "mock_url_instance"
        mock_query_get_by_id.return_value = "mock_query"
        mock_build_absolute_uri.return_value = mock_url_instance
        mock_oai_registry_get_by_id.return_value = mock_oai_registry

        self._send_request(
            {"id_query": "mock_id_query", "to_be_added": "false"}
        )
        mock_remove_oaipmh_data_source.assert_called_with(
            "mock_query",
            None,
            self.user,
        )

    @patch(
        "core_explore_oaipmh_app.views.user.ajax.oaipmh_query_api.remove_oaipmh_data_source"
    )
    @patch(
        "core_explore_oaipmh_app.views.user.ajax.oai_registry_api.get_by_id"
    )
    @patch("django.http.HttpRequest.build_absolute_uri")
    @patch("core_explore_oaipmh_app.views.user.ajax.api_query.get_by_id")
    def test_remove_oaipmh_data_source_fails_returns_400(
        self,
        mock_query_get_by_id,
        mock_build_absolute_uri,
        mock_oai_registry_get_by_id,
        mock_remove_oaipmh_data_source,
    ):
        """test_remove_oaipmh_data_source_fails_returns_400"""

        mock_oai_registry = MagicMock()
        mock_url_instance = "mock_url_instance"
        mock_query_get_by_id.return_value = "mock_query"
        mock_build_absolute_uri.return_value = mock_url_instance
        mock_oai_registry_get_by_id.return_value = mock_oai_registry
        mock_remove_oaipmh_data_source.side_effect = Exception(
            "mock_remove_oaipmh_data_source_exception"
        )

        self.assertEquals(
            self._send_request(
                {"id_query": "mock_id_query", "to_be_added": "false"}
            ).status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    @patch(
        "core_explore_oaipmh_app.views.user.ajax.oaipmh_query_api.remove_oaipmh_data_source"
    )
    @patch(
        "core_explore_oaipmh_app.views.user.ajax.oai_registry_api.get_by_id"
    )
    @patch("django.http.HttpRequest.build_absolute_uri")
    @patch("core_explore_oaipmh_app.views.user.ajax.api_query.get_by_id")
    def test_success_returns_200(
        self,
        mock_query_get_by_id,
        mock_build_absolute_uri,
        mock_oai_registry_get_by_id,
        mock_remove_oaipmh_data_source,
    ):
        """test_success_returns_200"""

        mock_oai_registry = MagicMock()
        mock_url_instance = "mock_url_instance"
        mock_query_get_by_id.return_value = "mock_query"
        mock_build_absolute_uri.return_value = mock_url_instance
        mock_oai_registry_get_by_id.return_value = mock_oai_registry
        mock_remove_oaipmh_data_source.return_value = None

        self.assertEquals(
            self._send_request(
                {"id_query": "mock_id_query", "to_be_added": "false"}
            ).status_code,
            status.HTTP_200_OK,
        )
