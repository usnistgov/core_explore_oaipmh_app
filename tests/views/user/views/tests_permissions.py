""" Permission tests on views
"""
from django.test import RequestFactory, override_settings

from core_explore_oaipmh_app.views.user.views import data_detail
from core_main_app.utils.integration_tests.integration_base_test_case import (
    IntegrationBaseTestCase,
)
from rest_framework import status
from unittest.mock import patch
from core_main_app.components.template.models import Template
from core_oaipmh_harvester_app.components.oai_record.models import OaiRecord
from core_oaipmh_harvester_app.components.oai_harvester_metadata_format.models import (
    OaiHarvesterMetadataFormat,
)
from core_main_app.utils.datetime import datetime_now
from core_oaipmh_harvester_app.components.oai_registry.models import (
    OaiRegistry,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from tests.fixtures.fixtures import AccessControlDataFixture


class TestViewData(IntegrationBaseTestCase):
    """Test View Data"""

    def setUp(self):
        """setUp"""

        self.factory = RequestFactory()
        self.user1 = create_mock_user(user_id="1")
        self.superuser = create_mock_user(user_id="2", is_superuser=True)
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

    @patch("core_explore_oaipmh_app.views.user.ajax.oai_record_api.get_by_id")
    def test_user_can_access_a_data(self, mock_record_get_by_id):
        """test_user_can_access_a_data"""
        oai_record = _create_oai_record()
        mock_record_get_by_id.return_value = oai_record
        request = self.factory.get("core_explore_oaipmh_app_data_detail")
        request.user = self.user1
        request.GET = {
            "id": str(oai_record.id),
        }
        response = data_detail(request)
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK,
        )

    @patch("core_explore_oaipmh_app.views.user.ajax.oai_record_api.get_by_id")
    def test_superuser_can_access_a_data(self, mock_record_get_by_id):
        """test_user_can_access_a_data"""
        oai_record = _create_oai_record()
        mock_record_get_by_id.return_value = oai_record
        request = self.factory.get("core_explore_oaipmh_app_data_detail")
        request.user = self.superuser
        request.GET = {
            "id": str(oai_record.id),
        }
        response = data_detail(request)
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK,
        )


def _create_oai_record():
    """Get an OaiRecord object.

    Returns:
        OaiRecord instance.

    """
    oai_record = OaiRecord()
    _set_oai_record_fields(oai_record)

    return oai_record


def _set_oai_record_fields(oai_record):
    """Set OaiRecord fields.

    Args:
        oai_record:

    Returns:
        OaiRecord with assigned fields.

    """
    oai_record.identifier = "oai:test/id.0006"
    oai_record.last_modification_date = datetime_now()
    oai_record.deleted = False
    oai_record.harvester_metadata_format = OaiHarvesterMetadataFormat()
    oai_record.registry = OaiRegistry()
    oai_record.harvester_metadata_format.template = Template(id=1)
    oai_record.xml_content = "<test><message>Hello</message></test>"

    return oai_record
