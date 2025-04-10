import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.store_page import StorePage
from utils.constants import PRODUCT_PAGE_URL


@pytest.mark.usefixtures("driver_init")
class TestAgeVerification:
    def test_age_verification_valid_alcohol(self):
        driver = self.driver
        store_page = StorePage(driver)

        # Open the Shop page and handle age verification with a valid birthdate.
        driver.get(PRODUCT_PAGE_URL)
        store_page.handle_age_verification("01-01-2000")
        time.sleep(2)

        try:
            confirmation = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@role='status' and contains(text(), 'You are of age')]")
                )
            ).text.strip()
        except TimeoutException:
            pytest.fail("Age verification confirmation not found.")
        assert "You are of age" in confirmation, "Age verification confirmation not found."

        # Click the Alcohol link from the left menu.
        driver.find_element(
            By.XPATH,
            "//div[contains(@class, 'widget widget-menu')]//ul/li/a[normalize-space()='Alocohol']"
        ).click()
        time.sleep(2)

        product_cards = driver.find_elements(By.XPATH, "//div[contains(@class, 'product-card')]")
        assert len(product_cards) > 0, "No alcohol product cards displayed for a valid user."

    def test_age_verification_underage(self):
        driver = self.driver
        store_page = StorePage(driver)

        # Open the Shop page and handle age verification with an underage birthdate.
        driver.get(PRODUCT_PAGE_URL)
        store_page.handle_age_verification("01-01-2008")
        time.sleep(2)

        try:
            error_msg = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@role='status' and contains(text(), 'You are underage')]")
                )
            ).text.strip()
        except TimeoutException:
            pytest.fail("Underage error message not displayed.")
        assert "You are underage" in error_msg, "Underage error message not found."

        # Click the Alcohol link from the left menu.
        driver.find_element(
            By.XPATH,
            "//div[contains(@class, 'widget widget-menu')]//ul/li/a[normalize-space()='Alocohol']"
        ).click()
        time.sleep(2)

        product_cards = driver.find_elements(By.XPATH, "//div[contains(@class, 'product-card')]")
        assert len(product_cards) == 0, "Alcohol product cards should not be displayed for underage users."
