from typing import Any
import unittest
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from models.insurance import INSURANCE_FUEL_VALUES as fuel
from services.scrapers.insurance import try_click
from services.scrapers.conversions import (
    wait_for_a_second,
    string_to_float_converter,
    insurance_engine_size_converter,
    insurance_power_converter,
)

test_insurance_data: dict[str, Any] = {
    "year": "2015",
    "engine_size": "2200",
    "fuel_type": fuel["gasoline"],
    "power": "150",
    "municipality": "София-град",
    "registration": False,
    "driver age": None,
    "driving experience": None,
}


class InsurancePageTest(unittest.TestCase):
    """Tests the url for scraping the price for insurace. If this test passes, there were no
    changes in the website's structure and the program can load insurance price successfully."""

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options=options)
        self.driver.get("https://www.sdi.bg/onlineinsurance/showQuestionnaire.php")

        # Consent button appears and prevents further action if not accepted
        try:
            self.driver.find_element(By.ID, "thinkconsent-button-accept-all").click()
        except Exception:
            pass

    def test_insurancePageLoadsSuccessfully(self):
        """Test if page loads successfully"""
        # Arrange & Act
        main_page = self.driver
        expected_title = "Калкулатор за Гражданска отговорност | SDI брокер"
        # Assert
        self.assertTrue(expected_title, main_page.title)

    def test_consentButtonExistance(self):
        """The consent button is clicked in the setUp method so trying to click it here
        should raise NoSuchElementException"""
        # Arrange, Act & Assert
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element(By.ID, "thinkconsent-button-accept-all").click()

    def test_pageSelectorsFilledCorrectly_returnsListOfPrices(self):
        """Submission form is divided into two pages and this test performs the actions on the first page"""
        # Arrange
        engine_size = insurance_engine_size_converter(test_insurance_data["engine_size"])
        power = insurance_power_converter(test_insurance_data["power"])
        # Act
        Select(self.driver.find_element(By.ID, "typeSelect")).select_by_value("1")
        Select(self.driver.find_element(By.ID, "dvigatelSelect")).select_by_value(
            engine_size
        )
        Select(self.driver.find_element(By.ID, "dvigatelType")).select_by_value(
            f'{test_insurance_data["fuel_type"]}'
        )
        Select(self.driver.find_element(By.ID, "ksiliSelect")).select_by_value(power)
        Select(self.driver.find_element(By.ID, "seatNumberSelect")).select_by_value("5")
        Select(
            self.driver.find_element(By.ID, "firstRegistrationYear")
        ).select_by_value(f'{test_insurance_data["year"]}')
        Select(self.driver.find_element(By.ID, "usefor")).select_by_value("1")
        if not test_insurance_data["registration"]:
            self.driver.find_element(By.ID, "noRegistration").send_keys("0")
        Select(self.driver.find_element(By.ID, "reg_no")).select_by_value("CA")

        wait_for_a_second(1)
        result = try_click(self.driver, "continue")
        wait_for_a_second(1)

        Select(self.driver.find_element(By.ID, "driverExperience")).select_by_value("5")
        Select(self.driver.find_element(By.ID, "where_go")).select_by_value("druga")

        try_click(self.driver, "calculate")
        wait_for_a_second()

        temp_prices = [
            string_to_float_converter(el.text.split("\n")[1])
            for el in self.driver.find_elements(By.CLASS_NAME, "oi-compare-row")
        ]
        # Assert
        self.assertIsNone(result)
        self.assertIsInstance(temp_prices, list)
        self.assertGreater(len(temp_prices), 2)

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
