import time
from unittest import TestCase

from response_api import create_app, main
from response_api.config import gunicorn
from response_api.util.api import time_count, time_second


class TestApiUtil(TestCase):

    def setUp(self) -> None:
        self.bind = "0.0.0.0:9000"
        self.app = create_app()

    def test_gunicorn_config(self):
        assert gunicorn.bind == self.bind

    def test_time_second(self):
        _time_1 = time_second()
        _time_2 = time.time()
        self.assertEqual(round(_time_1), round(_time_2))

    def test_time_count(self):
        _time_1 = time_second()
        _time_2 = time_count(_time_1)
        self.assertEqual(round(_time_2), round(time_second() - _time_1))

    def test_main_1(self):
        app = main.app
        self.assertEqual(self.app.title, app.title)
