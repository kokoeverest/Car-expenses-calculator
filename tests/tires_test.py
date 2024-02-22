import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import ElementClickInterceptedException
from time import sleep


class TiresPageTest(unittest.TestCase):
    '''Tests the url for scraping the tires information. If this test passes, there were no
        changes in the website's structure and the program can load tires prices successfully.'''

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless=new')
        self.driver = webdriver.Chrome(options=options)
        
        self.driver.get("https://www.bggumi.com/")

    def test_tiresPageLoadsSuccessfully(self):
        '''Test if page loads successfully'''

        # Arrange & Act
        main_page = self.driver
        expected_title = "bggumi.com -  Онлайн магазин за гуми - Най-големият избор на гуми и джанти."
        
        # Assert
        self.assertTrue(expected_title, main_page.title)

    def test_getWheelsizeElement_notAvailableImmediately(self):
        '''If no waits are added, the elements are not loaded and NoSuchElementException will be raised'''
        
        # Arrange, Act & Assert
        with self.assertRaises(ElementClickInterceptedException):
            self.driver.find_element(By.ID, 'get_wheelsize').click()

    def test_getWheelsizeElement_availableAfterAddingWaits(self):
        '''If waits are added between selecting by values, the elements will be loaded and the 
        get_wheelsize button will be clickable'''

        # Arrange & Act
        Select(self.driver.find_element(By.ID, "makers")).select_by_value('dacia')
        sleep(2)
        Select(self.driver.find_element(By.ID, "models")).select_by_value('duster')
        sleep(2)
        Select(self.driver.find_element(By.ID, "years")).select_by_value('2022')
        sleep(2)
        button = self.driver.find_element(By.ID, 'get_wheelsize').click()
        sleep(5)
        table = self.driver.find_element(By.CLASS_NAME, 'table')

        # Assert
        self.assertIsNone(button)
        self.assertIsNotNone(table)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()