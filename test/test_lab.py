import unittest
import cepimose
import datetime
from nose.plugins.attrib import attr


class CepimoseTestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_lab_start_timestamp(self):
        ts = cepimose.lab_start_timestamp()
        print("First NIJZ Covid-19 report:", ts)
        first_case = datetime.datetime(2020, 3, 4)
        today = datetime.datetime.now()

        self.assertEqual(first_case, ts)

    def test_lab_end_timestamp(self):
        ts = cepimose.lab_end_timestamp()
        print("Last update:", ts)
        day_delta = datetime.timedelta(days=3)
        today = datetime.datetime.now()
        diff = today - ts
        self.assertGreaterEqual(day_delta, diff)