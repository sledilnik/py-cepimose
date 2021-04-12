import unittest
import cepimose
import datetime


class CepimoseTestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def assertDatesIncreaseSince(self, data, startDate):
        previousDate = startDate - datetime.timedelta(days=1)
        for row in data:
            self.assertGreater(row.date, previousDate, row)
            previousDate = row.date

    def test_vaccinations_by_day(self):
        # Test feature one.
        data = cepimose.vaccinations_by_day()
        self.assertGreater(len(data), 100)

        def assertRow(row, expected_date, expected_first, expected_second):
            self.assertEqual(row.date, expected_date)
            self.assertAlmostEqual(row.first_dose, expected_first, delta=30)
            self.assertAlmostEqual(row.second_dose, expected_second, delta=30)

        #! NIJZ is changing data tests could fail in the future
        assertRow(data[9], datetime.datetime(2021, 1, 5), 15711, 0)
        assertRow(data[22], datetime.datetime(2021, 1, 18), 48711, 315)

        self.assertDatesIncreaseSince(data, datetime.datetime(2020, 12, 27))

    def test_vaccinations_by_age(self):
        # Test feature one.
        data = {row.age_group: row for row in cepimose.vaccinations_by_age()}

        expected_age_groups = [
            "0-17",
            "18-24",
            "25-29",
            "30-34",
            "35-39",
            "40-44",
            "45-49",
            "50-54",
            "55-59",
            "60-64",
            "65-69",
            "70-74",
            "75-79",
            "80-84",
            "85-89",
            "90+",
        ]

        self.assertTrue(len(data), len(expected_age_groups))

        for grp in expected_age_groups:
            self.assertGreater(data[grp].count_first, 0)
            self.assertGreater(data[grp].share_first, 0)
            self.assertGreater(data[grp].count_second, 0)
            self.assertGreater(data[grp].share_second, 0)

    def test_vaccinations_by_region(self):
        # Test feature one.
        data = {row.region: row for row in cepimose.vaccinations_by_region()}

        expected_regions = [
            "Koroška",
            "Zasavska",
            "Goriška",
            "Posavska",
            "Gorenjska",
            "Podravska",
            "Pomurska",
            "Osrednjeslovenska",
            "Jugovzhodna Slovenija",
            "Primorsko-notranjska",
            "Savinjska",
            "Obalno-kraška",
        ]

        print(data.keys())

        self.assertTrue(len(data), len(expected_regions))

        for grp in expected_regions:
            self.assertGreater(data[grp].count_first, 0)
            self.assertGreater(data[grp].share_first, 0)
            self.assertGreater(data[grp].count_second, 0)
            self.assertGreater(data[grp].share_second, 0)

    def test_vaccine_supply_and_usage(self):
        data = cepimose.vaccines_supplied_and_used()
        self.assertGreater(len(data), 100)

        def assertRow(row, expected_date, expected_supp, expected_used):
            self.assertEqual(row.date, expected_date)
            self.assertAlmostEqual(row.supplied, expected_supp, delta=30)
            self.assertAlmostEqual(row.used, expected_used, delta=30)

        #! NIJZ is changing data tests could fail in the future
        assertRow(data[9], datetime.datetime(2021, 1, 4), 39780, 13248)
        assertRow(data[22], datetime.datetime(2021, 1, 17), 60870, 48799)

        self.assertDatesIncreaseSince(data, datetime.datetime(2020, 12, 26))

    def test_supplied_by_manufacturer(self):
        data = cepimose.vaccines_supplied_by_manufacturer()
        self.assertTrue(len(data) > 10)

        def assertRow(row, expected_date, expected):
            self.assertEqual(row.date, expected_date)
            self.assertEqual(row.pfizer, expected[0])
            self.assertEqual(row.moderna, expected[1])
            self.assertEqual(row.az, expected[2])

        assertRow(data[1], datetime.datetime(2020, 12, 30), [8190, None, None])  # R = 2
        assertRow(data[3], datetime.datetime(2021, 1, 11), [19890, None, None])  # R = 6
        assertRow(
            data[16], datetime.datetime(2021, 2, 25), [None, 8400, 16800]
        )  # combined: two response data items with same date; second has R = 1

        self.assertDatesIncreaseSince(data, datetime.datetime(2020, 12, 26))

    def test_supplied_by_manufacturer_cumulative(self):
        data = cepimose.vaccines_supplied_by_manufacturer_cumulative()
        self.assertTrue(len(data) > 10)

        def assertRow(row, expected_date, expected):
            self.assertEqual(row.date, expected_date)
            self.assertEqual(row.pfizer, expected[0])
            self.assertEqual(row.moderna, expected[1])
            self.assertEqual(row.az, expected[2])

        assertRow(data[3], datetime.datetime(2021, 1, 11), [59670, None, None])
        assertRow(data[7], datetime.datetime(2021, 1, 31), [None, 3600, None])
        assertRow(data[10], datetime.datetime(2021, 2, 6), [None, None, 9600])
        assertRow(data[16], datetime.datetime(2021, 2, 25), [None, 16800, 52800])
        # assertRow(
        #     data[len(data) - 1], datetime.datetime(2021, 4, 2), [285480, 46800, 144000]
        # )  # this test will fail in the future

        self.assertDatesIncreaseSince(data, datetime.datetime(2020, 12, 26))

    def test_vaccinations_by_age_range_90(self):
        data = cepimose.vaccinations_by_age_range_90()
        data_dose1 = data.dose1
        data_dose2 = data.dose2

        self.assertTrue(len(data_dose1) > 10)
        self.assertTrue(len(data_dose2) > 10)
        self.assertTrue(len(data_dose1) > len(data_dose2))
        self.assertTrue(len(data_dose1) - len(data_dose2) == 12)

        def assertRow(row, expected_date, expected_dose):
            self.assertEqual(row.date, expected_date)
            self.assertAlmostEqual(row.dose, expected_dose, delta=30)

        assertRow(data_dose1[21], datetime.datetime(2021, 1, 17), 3580)
        assertRow(data_dose1[70], datetime.datetime(2021, 3, 7), 7866)
        assertRow(data_dose2[9], datetime.datetime(2021, 1, 17), 1)
        assertRow(data_dose2[58], datetime.datetime(2021, 3, 7), 4821)

        self.assertDatesIncreaseSince(data_dose1, datetime.datetime(2020, 12, 26))
        self.assertDatesIncreaseSince(data_dose2, datetime.datetime(2020, 12, 26))

    def test_vaccinations_by_age_rage(self):
        data = cepimose.vaccinations_by_age_range()
        expected_keys = [
            "0-17",
            "18-24",
            "25-29",
            "30-34",
            "35-39",
            "40-44",
            "45-49",
            "50-54",
            "55-59",
            "60-64",
            "65-69",
            "70-74",
            "75-79",
            "80-84",
            "85-90",
            "90+",
        ]

        self.assertEquals(expected_keys, list(data.keys()), "Object keys")

        range_90_data = data["90+"]
        data_dose1 = range_90_data.dose1
        data_dose2 = range_90_data.dose2

        self.assertTrue(len(data_dose1) > 10)
        self.assertTrue(len(data_dose2) > 10)
        self.assertTrue(len(data_dose1) > len(data_dose2))
        self.assertTrue(len(data_dose1) - len(data_dose2) == 12)

        def assertRow(row, expected_date, expected_dose):
            self.assertEqual(row.date, expected_date)
            self.assertAlmostEqual(row.dose, expected_dose, delta=30)

        assertRow(data_dose1[21], datetime.datetime(2021, 1, 17), 3580)
        assertRow(data_dose1[70], datetime.datetime(2021, 3, 7), 7866)
        assertRow(data_dose2[9], datetime.datetime(2021, 1, 17), 1)
        assertRow(data_dose2[58], datetime.datetime(2021, 3, 7), 4821)

        self.assertDatesIncreaseSince(data_dose1, datetime.datetime(2020, 12, 26))
        self.assertDatesIncreaseSince(data_dose2, datetime.datetime(2020, 12, 26))

    def test_vaccinations_pomurska_by_day(self):
        data = cepimose.vaccinations_pomurska_by_day()

        self.assertGreater(len(data), 100)

        def assertRow(row, expected_date, expected_first, expected_second):
            self.assertEqual(row.date, expected_date)
            self.assertAlmostEqual(row.first_dose, expected_first, delta=30)
            self.assertAlmostEqual(row.second_dose, expected_second, delta=30)

        assertRow(data[9], datetime.datetime(2021, 1, 5), 988, 0)
        assertRow(data[22], datetime.datetime(2021, 1, 18), 2847, 5)

        self.assertDatesIncreaseSince(data, datetime.datetime(2020, 12, 27))

    def test_vaccinations_by_region_by_day(self):
        data = cepimose.vaccinations_by_region_by_day()
        expected_keys = [
            "Goriška",
            "Zasavska",
            "Koroška",
            "Gorenjska",
            "Osrednjeslovenska",
            "Posavska",
            "Podravska",
            "Pomurska",
            "Savinjska",
            "Jugovzhodna Slovenija",
            "Primorsko-notranjska",
            "Obalno-kraška",
        ]

        self.assertEquals(expected_keys, list(data.keys()), "Object keys")

        for element in data.items():
            print(element[0])
            self.assertTrue(len(element[1]) != 0)
            self.assertDatesIncreaseSince(element[1], datetime.datetime(2020, 12, 27))

        pomurska_region = data["Pomurska"]

        def assertRow(row, expected_date, expected_first, expected_second):
            self.assertEqual(row.date, expected_date)
            self.assertAlmostEqual(row.first_dose, expected_first, delta=30)
            self.assertAlmostEqual(row.second_dose, expected_second, delta=30)

        assertRow(pomurska_region[9], datetime.datetime(2021, 1, 5), 988, 0)
        assertRow(pomurska_region[22], datetime.datetime(2021, 1, 18), 2847, 5)

    def test_vaccinations_by_municipalities_share(self):
        data = cepimose.vaccinations_by_municipalities_share()

        mun_number = 212

        self.assertTrue(len(data), mun_number)