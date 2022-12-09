""" Permission tests on views
"""
from django.test import RequestFactory, override_settings

from core_explore_oaipmh_app.views.user.views import data_detail
from core_main_app.utils.integration_tests.integration_base_test_case import (
    MongoIntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from tests.fixtures.fixtures import AccessControlDataFixture


class TestViewData(MongoIntegrationBaseTestCase):
    """Test View Data"""

    def setUp(self):
        """setUp"""

        self.factory = RequestFactory()
        self.user1 = create_mock_user(user_id="1")
        self.anonymous = create_mock_user(user_id=None, is_anonymous=True)
        self.fixture = AccessControlDataFixture()
        self.fixture.insert_data()

    @override_settings(CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT=False)
    def test_an_anonymous_user_can_not_access_a_data_that_is_not_in_a_workspace(
        self,
    ):
        """test_an_anonymous_user_can_not_access_a_data_that_is_not_in_a_workspace"""

        request = self.factory.get("core_explore_oaipmh_app_data_detail")
        request.user = self.anonymous
        request.GET = {
            "id": str(self.fixture.data_no_workspace.id),
        }
        response = data_detail(request)
        self.assertTrue(
            self.fixture.data_no_workspace.title
            not in response.content.decode()
        )
        self.assertTrue("Error 403" in response.content.decode())

    @override_settings(CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT=False)
    def test_an_anonymous_user_can_not_access_a_data_that_is_in_a_private_workspace(
        self,
    ):
        """test_an_anonymous_user_can_not_access_a_data_that_is_in_a_private_workspace"""

        request = self.factory.get("core_explore_oaipmh_app_data_detail")
        request.user = self.anonymous
        request.GET = {
            "id": str(self.fixture.data_workspace_1.id),
        }
        response = data_detail(request)
        self.assertTrue(
            self.fixture.data_workspace_1.title
            not in response.content.decode()
        )
        self.assertTrue("Error 403" in response.content.decode())

    @override_settings(CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT=False)
    def test_an_anonymous_user_can_not_access_a_data_that_is_in_a_public_workspace_and_access_setting_is_false(
        self,
    ):
        """test_an_anonymous_user_can_not_access_a_data_that_is_in_a_public_workspace_and_access_setting_is_false"""

        request = self.factory.get("core_explore_oaipmh_app_data_detail")
        request.user = self.anonymous
        request.GET = {
            "id": str(self.fixture.data_public_workspace.id),
        }
        response = data_detail(request)
        self.assertTrue(
            self.fixture.data_public_workspace.title
            not in response.content.decode()
        )
        self.assertTrue("Error 403" in response.content.decode())
