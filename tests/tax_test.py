import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import UnexpectedAlertPresentException


class TaxPageTest(unittest.TestCase):
    '''Tests the url for scraping the tax information. If this test passes, there were no
        changes in the website's structure and the program can load tax price successfully.'''

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless=new')
        self.driver = webdriver.Chrome()
        self.driver.get("https://cartax.uslugi.io/")

    def test_taxPageLoadsSuccessfully(self):
        '''Test if page loads successfully'''

        # Arrange & Act
        main_page = self.driver
        expected_title = "Калкулатор"
        
        # Assert
        self.assertTrue(expected_title, main_page.title)

    def test_submitButton_raisesAlert_ifNoValueInTheField(self):
        '''If no car power value is provided, an alert window will pop up and Selenium will 
        raise UnexpectedAlertPresentException'''
        # Arrange & Act 
        el = self.driver.find_element(By.XPATH, "//input[@name='kw']")
        el.clear()
        el.submit()
        # Assert
        with self.assertRaises(UnexpectedAlertPresentException):
            self.driver.find_element(By.CLASS_NAME, "amount").text.split(' ')[0]

    def test_submitButtonClick_worksWithCorrectValue(self):
        '''When car power data is entered in the field the form can be submitted'''
        car_power_data = {
            'kw': 136 # # should be "kw": car.engine.power_hp (if the power is not in kw - use the convertor)
        }
        # Arrange & Act
        for k, v in car_power_data.items():
            result = self.driver.find_element(By.XPATH, f"//input[@name='{k}']")
            result.clear()
            result.send_keys(v)
            result.submit()
        price = self.driver.find_element(By.CLASS_NAME, "amount").text.split(' ')[0]
        # Assert
        self.assertIsInstance(price, str)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()