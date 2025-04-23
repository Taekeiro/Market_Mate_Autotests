import pytest
import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.login_page import LoginPage
from pages.store_page import StorePage
from utils.constants import VALID_USER


@pytest.mark.usefixtures("driver_init")
class TestAgeVerification:
    def test_age_verification_valid(self):
        login = LoginPage(self.driver)
        store = StorePage(self.driver)

        # 0) Login
        login.open()
        login.login(VALID_USER['email'], VALID_USER['password'])
        time.sleep(1)

        # 1) Open shop & verify age ≥18
        store.open()
        store.handle_age_verification("01-01-2000")

        # 2) Check confirmation popup
        msg = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//div[@role='status' and contains(text(), 'You are of age')]")
        )).text
        assert "You are of age" in msg, "Expected age-confirmation message for 18+"

    def test_age_verification_underage(self):
        login = LoginPage(self.driver)
        store = StorePage(self.driver)

        # Login
        login.open()
        login.login(VALID_USER['email'], VALID_USER['password'])
        time.sleep(1)

        # Open shop & verify age <18
        store.open()
        store.handle_age_verification("01-01-2008")
        time.sleep(1)

        # Check underage popup
        msg = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH,
             "//div[@role='status' and contains(text(),"
             " 'You are underage. You can still browse')]")
        )).text
        assert "You are underage" in msg, "Expected underage warning"

        # Try opening alcohol section and ensure no alcohol cards
        store.open_alcohol_section()
        with pytest.raises(TimeoutException):
            # should time out finding any product cards
            self.wait.until(EC.presence_of_element_located(StorePage.PRODUCT_CARDS))
