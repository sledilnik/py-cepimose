import unittest
from unittest.case import skip
import cepimose
import datetime


class CepimoseTestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_schools_timestamp(self):
        ts = cepimose.schools_timestamp()
        self.assertIsInstance(ts, datetime.datetime)
        print("Last update:", ts)
        day_delta = datetime.timedelta(days=7)
        today = datetime.datetime.now()
        diff = today - ts
        self.assertGreaterEqual(day_delta, diff)

    @skip
    def test_schools_date_range_timestamps(self):
        data = cepimose.schools_date_range_timestamps()

    @skip
    def test_schools_confirmed_and_active_cases(self):
        data = cepimose.schools_confirmed_and_active_cases()

    @skip
    def test_schools_age_group(self):
        data = cepimose.schools_age_group()

    @skip
    def test_schools_age_group_confirmed_weekly(self):
        data = cepimose.schools_age_group_confirmed_weekly()

    @skip
    def test_schools_age_groups_triada(self):
        data = cepimose.schools_age_groups_triada()

    @skip
    def test_schools_age_group_percent_per_capita_weekly(self):
        data = cepimose.schools_age_group_percent_per_capita_weekly()

    @skip
    def test_schools_age_groups_percent_triada_weekly(self):
        data = cepimose.schools_age_groups_percent_triada_weekly()

    @skip
    def test_schools_age_group_percent_weekly(self):
        data = cepimose.schools_age_group_percent_weekly()