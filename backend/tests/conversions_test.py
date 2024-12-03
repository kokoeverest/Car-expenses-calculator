import unittest
from datetime import datetime
from services.scrapers import conversions as con
import test_data as td


class ConversionsTests(unittest.TestCase):
    def test_waitForASecond_sleepsForOneSecond_ifNotDefaultValueIsUsed(self):
        # Arrange
        seconds_to_sleep = 1

        # Act
        start_of_function = datetime.now()
        con.wait_for_a_second(seconds_to_sleep)
        end_of_function = datetime.now()
        
        actual_result = end_of_function - start_of_function

        # Assert
        self.assertEqual(actual_result.seconds, seconds_to_sleep)

    def test_findCorrectName_returns_theMostAppropriateResult(self):
        # Arrange & Act
        actual_result = con.find_correct_name(
            td.sample_car_model, td.sample_car_model_options
        )

        # Assert
        self.assertGreater(len(actual_result), 0)

    def test_wordVersions_returns_dictWithWordVersions(self):
        # Arrange & Act
        actual_result = con.word_versions(td.sample_car_brand)

        # Assert
        self.assertIsInstance(actual_result, set)
        self.assertGreater(len(actual_result), 0)

    def test_calculateAge_returnsCorrectAge_fromYearString(self):
        # Arrange
        year_string = "2010"
        expected_result = datetime.now().year - int(year_string)

        # Act
        actual_result = con.calculate_age(year_string)

        # Assert
        self.assertEqual(actual_result, expected_result)

    def test_ageConverter_ReturnsCorrectNumbers_fromAges(self):
        # Arrange
        expected_result = ["0", "1", "2", "3", "4"]

        # Act
        actual_result = [con.tax_age_converter(age) for age in td.sample_car_ages]

        # Assert
        self.assertListEqual(actual_result, expected_result)

    def test_getEuroCategoryFromCarAge_returnsCorrectValues(self):
        # Arrange
        expected_result = [
            "EEV",
            "без екологична категория",
            "Euro 1",
            "Euro 2",
            "Euro 3",
            "Euro 4",
            "Euro 5",
            "Euro 6",
        ]

        # Act
        actual_result = [
            con.tax_get_euro_category_from_car_year(year) for year in td.sample_car_years
        ]

        # Assert
        self.assertListEqual(actual_result, expected_result)

    def test_hpToKwConverter_returns_correctResult(self):
        # Arrange
        expected_result = "101"

        # Act
        actual_result = con.hp_to_kw_converter(td.sample_car_power_hp)

        # Assert
        self.assertEqual(actual_result, expected_result)

    def test_kwToHpConverter_returns_correctResult(self):
        # Arrange
        expected_result = "135"

        # Act
        actual_result = con.kw_to_hp_converter(td.sample_car_power_kw)

        # Assert
        self.assertEqual(actual_result, expected_result)

    def test_validateEngineCapacity_returnsCorrectCapacity_fromVariousInputs(self):
        # Arrange
        expected_result = "2400"

        # Act & Assert
        for capacity in td.sample_engine_capacities:
            self.assertEqual(expected_result, con.validate_engine_capacity(capacity))

    def test_carStringConverter_returns_correctlyFormattedString(self):
        # Arrange
        expected_result = "mercedes-benz"

        # Act
        actual_result = con.car_string_converter(td.sample_car_brand)

        # Assert
        self.assertEqual(actual_result, expected_result)

    def test_priceConverter_returns_correctlyConvertedPrices_withValidInputs(self):
        # Arrange
        excpected_result = 1234.56

        # Act & Assert
        for price in td.valid_product_prices:
            actual_result = con.string_to_float_converter(price)
            self.assertEqual(actual_result, excpected_result)
            self.assertIsInstance(actual_result, float)

    def test_priceConverter_returs_zeroFloat_withInvalidInput(self):
        # Arrange
        excpected_result = 0.0

        # Act
        actual_result = con.string_to_float_converter(td.invalid_product_price)

        # Assert
        self.assertEqual(actual_result, excpected_result)
        self.assertIsInstance(actual_result, float)

    def test_engineSizeConverter_returns_correctValues_fromVariousInputs(self):
        # Arrange
        expected_result = ["800", "2000", "3000", "3200", "3500", "3501"]

        # Act
        actual_result = [
            con.insurance_engine_size_converter(size) for size in td.sample_engine_sizes
        ]

        # Assert
        self.assertListEqual(actual_result, expected_result)

    def test_insurancePowerConverter_returns_correctValues_fromVariousInputs(self):
        # Arrange
        expected_result = ["66", "74", "75", "88", "110", "118", "125", "126"]

        # Act
        actual_result = [
            con.insurance_power_converter(power) for power in td.sample_engine_powers
        ]

        # Assert
        self.assertListEqual(actual_result, expected_result)

    def test_done_returns_defaultString(self):
        # Arrange
        sample_string = "Sample"

        # Act & Assert
        self.assertIsNone(con.done())
        self.assertIsNone(con.done(sample_string))

    def test_fuelStringConverter_returns_correctFuelTypes(self):
        # Arrange
        expected_result = [
            "Electricity",
            "CNG",
            "LPG",
            "Plug-in hybrid gasoline",
            "Plug-in hybrid diesel",
            "Gasoline",
            "Diesel",
        ]

        # Act
        actual_result = [
            con.fuel_string_converter(fuel_type) for fuel_type in td.sample_fuel_types
        ]

        # Assert
        self.assertListEqual(actual_result, expected_result)
