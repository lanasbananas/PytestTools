from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import unittest
import pytest

class TestRegistration(unittest.TestCase):
    def setLink(self, link):
        self.browser.get(link)

    @classmethod
    def setUpClass(cls):
        cls.browser = webdriver.Chrome()
        #cls.browser.get(cls.link)

    @classmethod
    def tearDownClass(cls):
        time.sleep(5)
        cls.browser.quit()

    def test_registration_1(self):
        self.setLink("https://suninjuly.github.io/registration1.html")
        input1 = self.browser.find_element(By.CSS_SELECTOR, '[placeholder="Input your first name"]')
        input1.send_keys("Ivan")
        input2 = self.browser.find_element(By.CSS_SELECTOR, '[placeholder="Input your last name"]')
        input2.send_keys("Petrov")
        input3 = self.browser.find_element(By.CSS_SELECTOR, '[placeholder="Input your email"]')
        input3.send_keys("Email")
        button = self.browser.find_element(By.CSS_SELECTOR, "button.btn")
        button.click()
        time.sleep(1)

        welcome_text_elt = self.browser.find_element(By.TAG_NAME, "h1")
        welcome_text = welcome_text_elt.text

        self.assertEqual("Congratulations! You have successfully registered!", welcome_text, "Texts don't match")

    def test_registration_2(self):
        self.setLink("https://suninjuly.github.io/registration2.html")
        input1 = self.browser.find_element(By.CSS_SELECTOR, '[placeholder="Input your first name"]')
        input1.send_keys("Ivan")
        input2 = self.browser.find_element(By.CSS_SELECTOR, '[placeholder="Input your last name"]')
        input2.send_keys("Petrov")
        input3 = self.browser.find_element(By.CSS_SELECTOR, '[placeholder="Input your email"]')
        input3.send_keys("Email")

        button = self.browser.find_element(By.CSS_SELECTOR, "button.btn")
        button.click()
        time.sleep(1)

        welcome_text_elt = self.browser.find_element(By.TAG_NAME, "h1")
        welcome_text = welcome_text_elt.text

        self.assertEqual("Congratulations! You have successfully registered!", welcome_text, "Texts don't match")


if __name__ == "__main__":
    unittest.main()