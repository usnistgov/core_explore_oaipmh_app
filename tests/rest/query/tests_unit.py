""" Unit tests for Explore OAI-PMH REST API
"""

from unittest.mock import patch, MagicMock

from django.core import paginator as django_paginator
from django.test import SimpleTestCase, tag, override_settings

from core_explore_oaipmh_app.rest.query import views as query_views
from core_main_app.commons.exceptions import ApiError
from core_main_app.utils.pagination.mongoengine_paginator import (
    paginator as mongo_paginator,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import (
    create_mock_request,
)


class TestExecuteExecuteOaiPmhQuery(SimpleTestCase):
    """TestExecuteExecuteOaiPmhQuery"""

    @patch(
        "core_oaipmh_harvester_app.components.oai_registry.api.get_all_activated_registry"
    )
    @patch(
        "core_oaipmh_harvester_app.components.oai_record.api.execute_json_query"
    )
    def test_execute_local_query_returns_page_of_results(
        self, mock_execute_json_query, mock_get_all_activated_registry
    ):
        """test_execute_local_query_returns_page_of_results

        Returns:

        """
        # Arrange
        mock_user = create_mock_user(1)
        mock_query_data = {"query": {}}
        mock_request = create_mock_request(user=mock_user)
        mock_queryset = MagicMock()
        mock_execute_json_query.return_value = mock_queryset
        mock_activated_registries_response = MagicMock()
        mock_activated_registries_response.values_list.return_value = []
        mock_get_all_activated_registry.return_value = (
            mock_activated_registries_response
        )

        # Act
        page = query_views.execute_oaipmh_query(
            query_data=mock_query_data, page=1, request=mock_request
        )

        # Assert
        self.assertTrue(isinstance(page, django_paginator.Page))
        self.assertTrue(isinstance(page.paginator, django_paginator.Paginator))

    @patch(
        "core_oaipmh_harvester_app.components.oai_harvester_metadata_format.api.get_all_by_list_registry_ids"
    )
    @patch(
        "core_oaipmh_harvester_app.components.oai_registry.api.get_all_activated_registry"
    )
    @patch(
        "core_oaipmh_harvester_app.components.oai_record.api.execute_json_query"
    )
    def test_execute_oaipmh_query_with_params_returns_page_of_results(
        self,
        mock_execute_json_query,
        mock_get_all_activated_registry,
        mock_get_all_by_list_registry_ids,
    ):
        """test_execute_oaipmh_query_returns_page_of_results

        Returns:

        """
        # Arrange
        mock_user = create_mock_user(1)
        mock_query_data = {
            "query": {},
            "templates": '[{"id": 1}]',
            "options": '{"visibility": "public", "instance_id": "1"}',
            "order_by_field": "[]",
        }
        mock_request = create_mock_request(user=mock_user)
        mock_queryset = MagicMock()
        mock_execute_json_query.return_value = mock_queryset
        mock_activated_registries_response = MagicMock()
        mock_activated_registries_response.values_list.return_value = []
        mock_get_all_activated_registry.return_value = (
            mock_activated_registries_response
        )
        mock_all_by_list_ids_response = MagicMock()
        mock_all_by_list_ids_response.values_list.return_value = []
        mock_get_all_by_list_registry_ids.return_value = (
            mock_all_by_list_ids_response
        )
        # Act
        page = query_views.execute_oaipmh_query(
            query_data=mock_query_data, page=1, request=mock_request
        )

        # Assert
        self.assertTrue(isinstance(page, django_paginator.Page))
        self.assertTrue(mock_get_all_activated_registry.called)
        self.assertTrue(mock_get_all_by_list_registry_ids.called)

    @tag("mongodb")
    @override_settings(MONGODB_INDEXING=True)
    @patch(
        "core_oaipmh_harvester_app.components.oai_registry.api.get_all_activated_registry"
    )
    @patch(
        "core_oaipmh_harvester_app.components.oai_record.api.execute_json_query"
    )
    def test_execute_local_query_returns_page_of_mongo_results(
        self, mock_execute_json_query, mock_get_all_activated_registry
    ):
        """test_execute_local_query_returns_page_of_mongo_results

        Returns:

        """
        # Arrange
        mock_user = create_mock_user(1)
        mock_query_data = {"query": {}}
        mock_request = create_mock_request(user=mock_user)
        mock_queryset = MagicMock()
        mock_queryset.count.return_value = 0
        mock_execute_json_query.return_value = mock_queryset
        mock_activated_registries_response = MagicMock()
        mock_activated_registries_response.values_list.return_value = []
        mock_get_all_activated_registry.return_value = (
            mock_activated_registries_response
        )

        # Act
        page = query_views.execute_oaipmh_query(
            query_data=mock_query_data, page=1, request=mock_request
        )

        # Assert
        self.assertTrue(isinstance(page, django_paginator.Page))
        self.assertTrue(
            isinstance(page.paginator, mongo_paginator.MongoenginePaginator)
        )

    def test_execute_oaipmh_query_none_raises_api_error(self):
        """test_execute_oaipmh_query_none_raises_api_error

        Returns:

        """
        # Arrange
        mock_user = create_mock_user(1)
        mock_query_data = {}
        mock_request = create_mock_request(user=mock_user)

        # Act + Assert
        with self.assertRaises(ApiError):
            query_views.execute_oaipmh_query(
                query_data=mock_query_data, page=1, request=mock_request
            )


class TestFormatOaiPmhResults(SimpleTestCase):
    """TestFormatOaiPmhResults"""

    def test_format_oaipmh_empty_results_returns_empty_list(
        self,
    ):
        """test_format_oaipmh_empty_results_returns_empty_list

        Returns:

        """
        # Arrange
        mock_user = create_mock_user(1)
        mock_results = MagicMock()
        mock_results.object_list = []
        mock_request = create_mock_request(user=mock_user)

        # Act
        results = query_views.format_oaipmh_results(
            results=mock_results, request=mock_request
        )

        # Assert
        self.assertIsInstance(results, list)

    @override_settings(INSTALLED_APPS=[])
    def test_format_oaipmh_results_returns_list(
        self,
    ):
        """test_format_oaipmh_results_returns_list

        Returns:

        """
        # Arrange
        mock_user = create_mock_user(1)
        mock_data = MagicMock()
        mock_data.template_id = 1
        mock_harvester_metadata_format = MagicMock()
        mock_harvester_metadata_format.id = 1
        mock_harvester_metadata_format.name = "metadata_format_name"
        mock_data.harvester_metadata_format = mock_harvester_metadata_format
        mock_results = MagicMock()
        mock_results.object_list = [mock_data]
        mock_request = create_mock_request(user=mock_user)

        # Act
        results = query_views.format_oaipmh_results(
            results=mock_results, request=mock_request
        )

        # Assert
        self.assertIsInstance(results, list)
        self.assertTrue(len(results), 1)
