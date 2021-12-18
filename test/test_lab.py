from cepimose.types import LabDashboard
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

    @attr("sledilnik")
    def test_lab_PCR_tests_performed(self):
        performed_PCR = cepimose.lab_PCR_tests_performed()
        self.assertGreaterEqual(performed_PCR, 0)
        self.assertLessEqual(performed_PCR, 15000)

    def test_lab_PCR_total_tests_performed(self):
        performed_PCR_total = cepimose.lab_PCR_total_tests_performed()
        self.assertGreaterEqual(performed_PCR_total, 1600000)
        self.assertLessEqual(performed_PCR_total, 1000000000)

    def test_lab_active_cases_estimated(self):
        active_cases_estimated = cepimose.lab_active_cases_estimated()
        self.assertGreaterEqual(active_cases_estimated, 0)
        self.assertLessEqual(active_cases_estimated, 2100000)

    def test_lab_confirmed_total_male(self):
        male_total = cepimose.lab_confirmed_total_male()
        self.assertGreaterEqual(male_total, 140000)
        self.assertLessEqual(male_total, 1000000000)

    def test_lab_total_vaccinated_first_dose(self):
        total_first_dose = cepimose.lab_total_vaccinated_first_dose()
        self.assertGreaterEqual(total_first_dose, 1180000)
        self.assertLessEqual(total_first_dose, 2100000)

    def test_lab_active_cases_100k(self):
        active_cases_100k = cepimose.lab_active_cases_100k()
        self.assertGreaterEqual(active_cases_100k, 0)
        self.assertLessEqual(active_cases_100k, 10000)
        self.assertIsInstance(active_cases_100k, float)

    def test_lab_cases_total_confirmed(self):
        cases_total = cepimose.lab_cases_total_confirmed()
        self.assertGreaterEqual(cases_total, 250000)

    def test_lab_HAT_total_tests_performed(self):
        performed_HAT = cepimose.lab_HAT_total_tests_performed()
        self.assertGreaterEqual(performed_HAT, 6500000)
        self.assertLessEqual(performed_HAT, 1000000000)

    @attr("sledilnik")
    def test_lab_cases_confirmed(self):
        cases_confirmed = cepimose.lab_cases_confirmed()
        self.assertGreaterEqual(cases_confirmed, 0)
        self.assertLessEqual(cases_confirmed, 10000)

    def test_lab_confirmed_total_female(self):
        female_total = cepimose.lab_confirmed_total_female()
        self.assertGreaterEqual(female_total, 160000)
        self.assertLessEqual(female_total, 1000000000)

    def test_lab_total_vaccinated_fully(self):
        fully_vaccinated = cepimose.lab_total_vaccinated_fully()
        self.assertGreaterEqual(fully_vaccinated, 1100000)
        self.assertLessEqual(fully_vaccinated, 2100000)

    def test_lab_cases_avg_7Days(self):
        cases_avg_7days = cepimose.lab_cases_avg_7Days()
        self.assertGreaterEqual(cases_avg_7days, 0)
        self.assertLessEqual(cases_avg_7days, 15000)

    @attr("sledilnik")
    def test_lab_HAT_tests_performed(self):
        performed_HAT = cepimose.lab_HAT_tests_performed()
        self.assertGreaterEqual(performed_HAT, 0)
        self.assertLessEqual(performed_HAT, 200000)

    def test_get_lab_dashboard(self):
        dashboard = cepimose.get_lab_dashboard()
        self.assertIsInstance(dashboard, LabDashboard)
