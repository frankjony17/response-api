
from unittest import TestCase, mock

from response_api.model.schema import (Response,
                                       ResponseBatchInput)
from response_api.service.client import Client


def test_commit():
    pass


class TestService(TestCase):

    def setUp(self) -> None:
        self.schema = ResponseBatchInput(
            system_client_name="FKS",
            fksolutions_service_name="TEST",
            response_number=0
        )
        self.db = mock.MagicMock(commit=test_commit)
        self.response = [Response(token_service='', client_identifier='',
                                  response_service={}, response_status=0)]

    def test_find_all_by_batch_1(self):
        client = Client(self.db)
        test = client.find_all_by_batch(self.schema)
        self.assertEqual(test[0], [])

    def test_find_all_by_batch_2(self):
        client = Client(self.db)
        schema = self.schema
        schema.response_number = 1
        test = client.find_all_by_batch(schema)
        self.assertEqual(test[0], [])

    def test_find_all_by_batch_3(self):
        client = Client(self.db)
        path = "response_api.repository.service." \
               "ResponseServiceRepository.find_all_by_system_and_service"

        with mock.patch(path, return_value=None):
            test = client.find_all_by_batch(self.schema)
        self.assertEqual(test[0], [])

    def tearDown(self) -> None:
        del self.schema
