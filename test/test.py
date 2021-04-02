import unittest
import cepimose
import datetime

class MyTestCase1(unittest.TestCase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_vaccinations_by_day(self):
        # Test feature one.
        data = cepimose.vaccinations_by_day()
        self.assertTrue(len(data) > 30)

        def assertRow(row, expected_date, expected_first, expected_second):
            self.assertEqual(row.date, expected_date)
            self.assertEqual(row.first_dose, expected_first)
            self.assertEqual(row.second_dose, expected_second)

        assertRow(data[9], datetime.datetime(2021, 1, 5, 1, 0), 15711, 0)
        assertRow(data[22], datetime.datetime(2021, 1, 18, 1, 0), 48710, 315)

    def test_vaccinations_by_age(self):
        # Test feature one.
        data = cepimose.vaccinations_by_age()
        self.assertTrue(len(data) > 30)

        def assertRow(row, expected_date, expected_first, expected_second):
            self.assertEqual(row.date, expected_date)
            self.assertEqual(row.first_dose, expected_first)
            self.assertEqual(row.second_dose, expected_second)

        assertRow(data[9], datetime.datetime(2021, 1, 5, 1, 0), 15711, 0)
        assertRow(data[22], datetime.datetime(2021, 1, 18, 1, 0), 48710, 315)