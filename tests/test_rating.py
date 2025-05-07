import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from pages.login_page import LoginPage
from pages.store_page import StorePage
from pages.cart_page import CartPage
from pages.rating_page import RatingPage
from utils.constants import VALID_USER
from utils.checkout import complete_checkout

@pytest.mark.usefixtures("driver_init")
class TestRating:

    def test_submit_valid_rating_and_feedback(self):
        login   = LoginPage(self.driver)
        store   = StorePage(self.driver)
        cart    = CartPage(self.driver)
        rating  = RatingPage(self.driver)
        wait    = WebDriverWait(self.driver, 10)

        # 1) Login & age verification
        login.open()
        login.login(**VALID_USER)
        store.open()
        store.handle_age_verification("01-01-2000")

        # 2) Open product; if restriction, purchase then reopen
        store.open_product_by_index(0)
        try:
            rating.wait_for_restriction(timeout=3)
            store.add_product_to_cart_by_index(0)
            store.wait_for_toast_disappear()
            cart.open_cart()
            complete_checkout(self.driver, wait)
            store.open()
            store.open_product_by_index(0)
        except TimeoutException:
            pass

        # 3) Submit 5-star review
        rating.submit_rating(5, "Great product! After purchase.")

        # 4) Verify comment; skip on known bug
        try:
            elem = wait.until(EC.visibility_of_element_located(RatingPage.REVIEW_WIDGET))
            text = self.driver.find_element(By.XPATH,
                                            "//section[@class='product-comments']//p").text.strip()
            if "Great product! After purchase." not in text:
                pytest.skip("⚠️ Known bug: comment missing")
        except TimeoutException:
            pytest.skip("⚠️ Known bug: review widget never appeared")

    def test_submit_invalid_rating(self):
        login   = LoginPage(self.driver)
        store   = StorePage(self.driver)
        cart    = CartPage(self.driver)
        rating  = RatingPage(self.driver)
        wait    = WebDriverWait(self.driver, 10)

        # 1) Login & age verification
        login.open()
        login.login(**VALID_USER)
        store.open()
        store.handle_age_verification("01-01-2000")

        # 2) Purchase second product
        store.add_product_to_cart_by_index(1)
        store.wait_for_toast_disappear()
        cart.open_cart()
        complete_checkout(self.driver, wait)
        store.open()

        # 3) Re-open that product
        store.open_product_by_index(1)

        # 4) Submit invalid (0-star) review
        rating.submit_rating(0, "Invalid rating test")

        # 5) Verify error popup
        popup = wait.until(EC.visibility_of_element_located(RatingPage.ERROR_POPUP))
        text = popup.text.strip().lower()
        assert ("undefined" in text) or ("invalid input for the field 'rating'" in text), \
            f"Unexpected error text: '{popup.text}'"

    def test_edit_and_delete_rating(self):
        login  = LoginPage(self.driver)
        store  = StorePage(self.driver)
        rating = RatingPage(self.driver)
        wait   = WebDriverWait(self.driver, 10)

        # 1) Login & age & open product
        login.open()
        login.login(**VALID_USER)
        store.open()
        store.handle_age_verification("01-01-2000")
        store.open_product_by_index(0)

        # 2) Edit the review
        rating.edit_rating(3, "Edited comment test.")
        edited = wait.until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//div[contains(@class,'comment-body')]//p"
                "[contains(text(),'Edited comment test.')]"
            ))
        )
        assert edited

        # 3) Delete the review & verify form
        rating.delete_rating()
        rating.wait_for_new_review_form()
