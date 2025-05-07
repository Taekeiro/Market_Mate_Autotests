import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from pages.login_page import LoginPage
from pages.store_page import StorePage
from utils.constants import VALID_USER


@pytest.mark.usefixtures("driver_init")
class TestAgeVerification:
    def test_age_verification_valid(self):
        store = StorePage(self.driver)
        store.open()

        # 1) Enter valid birthdate and confirm
        store.handle_age_verification("01-01-2000")

        # 2) Verify the confirmation popup appears with the expected text
        confirmation = store.wait_for_visible((
            By.XPATH,
            "//div[@role='status' and contains(.,"
            " 'You are of age. You can now view all products, even alcohol products.')]"
        ))
        assert "You are of age" in confirmation.text, (
            "Expected age-confirmation message for 18+"
        )

        # 3) Finally, ensure the age-modal itself is gone
        with pytest.raises(TimeoutException):
            store.wait_for_visible(StorePage.AGE_MODAL)

    def test_age_verification_underage(self):
        login = LoginPage(self.driver)
        store = StorePage(self.driver)

        # login first
        login.open()
        login.login(VALID_USER['email'], VALID_USER['password'])

        # open store and enter underage birthdate
        store.open()
        store.handle_age_verification("01-01-2008")
        # verify underage message
        underage = store.wait_for_visible((
            By.XPATH,
            "//div[@role='status' and contains(text(),'You are underage')]"
        ))
        assert "You are underage" in underage.text

        # try to open Alcohol section and ensure no products appear
        store.open_alcohol_section()
        with pytest.raises(TimeoutException):
            store.wait_for_visible(StorePage.PRODUCT_CARDS)
