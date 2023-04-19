""" Permission tests on ajax
"""
from django.test import RequestFactory

from core_explore_oaipmh_app.views.user.ajax import (
    get_data_source_list_oaipmh,
    update_data_source_list_oaipmh,
)
from core_main_app.utils.integration_tests.integration_base_test_case import (
    IntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from tests.fixtures.fixtures import AccessControlDataFixture


class TestGetDataSourceListOaipmh(IntegrationBaseTestCase):
    """Test Get Data Source List Oaipmh"""

    def setUp(self):
        """setUp"""

        self.factory = RequestFactory()
        self.user1 = create_mock_user(user_id="1")
        self.anonymous = create_mock_user(user_id=None, is_anonymous=True)
        self.fixture = AccessControlDataFixture()
        self.fixture.insert_data()

    def test_an_anonymous_user_can_not_access_data_sources_of_a_user_query(
        self,
    ):
        """test_an_anonymous_user_can_not_access_data_sources_of_a_user_query"""

        request = self.factory.get("core_explore_oaipmh_app_get_data_sources")
        request.user = self.anonymous
        request.GET = {"id_query": str(self.fixture.query_user1.id)}
        response = get_data_source_list_oaipmh(request)
        self.assertEqual(response.status_code, 403)


class TestUpdateDataSourceListOaipmh(IntegrationBaseTestCase):
    """Test Update Data Source List Oaipmh"""

    def setUp(self):
        """setUp"""

        self.factory = RequestFactory()
        self.user1 = create_mock_user(user_id="1")
        self.anonymous = create_mock_user(user_id=None, is_anonymous=True)
        self.fixture = AccessControlDataFixture()
        self.fixture.insert_data()

    def test_an_anonymous_user_can_not_access_data_sources_of_a_user_query(
        self,
    ):
        """test_an_anonymous_user_can_not_access_data_sources_of_a_user_query"""

        request = self.factory.get(
            "core_explore_oaipmh_app_update_data_sources"
        )
        request.user = self.anonymous
        request.GET = {"id_query": str(self.fixture.query_user1.id)}
        response = update_data_source_list_oaipmh(request)
        self.assertEqual(response.status_code, 403)
