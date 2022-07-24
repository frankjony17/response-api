
from unittest import TestCase, mock

from response_api.repository.service import ResponseServiceRepository


def test_commit():
    pass


class TestRepository(TestCase):

    def test_update_response_number(self):
        path = "response_api.repository.service.ResponseServiceRepository.find_max_response_number"
        db = mock.MagicMock(commit=test_commit)
        response = [mock.MagicMock(ResponseService=mock.MagicMock(id=5))]  # res.ResponseService.id

        with mock.patch(path, return_value=0):
            repo = ResponseServiceRepository(db)
            self.assertEqual(repo.update_response_number(response), None)

    def test_update_by_token_response_number(self):
        path = "response_api.repository.service.ResponseServiceRepository.find_max_response_number"
        db = mock.MagicMock(commit=test_commit)

        with mock.patch(path, return_value=0):
            repo = ResponseServiceRepository(db)
            self.assertEqual(repo.update_by_token_response_number(5), None)
