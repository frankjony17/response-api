
from unittest import TestCase, mock

from fastapi.testclient import TestClient

from response_api import create_app
from response_api.model.database import ResponseService
from response_api.model.schema import Response


class TestRouter(TestCase):

    def setUp(self) -> None:
        app = create_app()
        self.client = TestClient(app)
        self.response = [Response(token_service='', client_identifier='',
                                  response_service={}, response_status=0)]
        self.data = {
            "system_client_name": "TEST",
            "fksolutions_service_name": "Python",
            "response_number": 0
        }

    def test_endpoint_welcome(self):
        response = self.client.get('/')
        assert response.status_code == 200

    def test_endpoint_health(self):
        response = self.client.get('/health')
        assert response.status_code == 200

    def test_endpoint_get_by_batch_1(self):
        path = "response_api.service.client.Client.find_all_by_batch"
        with mock.patch(path, return_value=(self.response, False)):
            response = self.client.post(url='/response/get-by-batch', json=self.data)
        self.assertEqual(response.status_code, 200)

    def test_endpoint_get_by_batch_2(self):
        response = self.client.post(url='/response/get-by-batch', json=self.data)
        self.assertEqual(response.status_code, 444)

    def test_endpoint_get_by_token(self):
        resp = ResponseService()
        resp.response_service = "processing"
        resp_mock = mock.MagicMock(ResponseService=resp)
        serv = mock.MagicMock(
            response_id=202103010000001,
            client_identifier="FK17",
            ResponseService=resp_mock,
            response_in_progress=False
        )
        path = "response_api.client.Client.find_by_token"

        with mock.patch(path, return_value=(serv, False)):
            response = self.client.post(url='/response/get-by-token', json={
                "token_service": "202103010000001",
                "client_identifier": "FK17"
            })
            self.assertEqual(response.status_code, 200)

    def test_endpoint_create_first(self):
        response = self.client.post(url='/response/create', json={
                "system_client_name": "TEST",
                "fksolutions_service_name": "Python",
                "system_client_identifier": "asdfg"
        })
        self.assertEqual(response.status_code, 444)

    def test_endpoint_update_service(self):
        response = self.client.post(url='/response/update', json={
                "response_id": 0,
                "response_service": {"teste": "OK"},
                "response_status": 200
        })
        self.assertEqual(response.status_code, 444)

    def tearDown(self) -> None:
        del self.client
        del self.response
        del self.data
