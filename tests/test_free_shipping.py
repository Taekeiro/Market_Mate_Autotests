import pytest
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from pages.login_page import LoginPage
from pages.store_page import StorePage
from pages.cart_page import CartPage
from utils.constants import VALID_USER

@pytest.mark.usefixtures("driver_init")
class TestFreeShipping:
    def test_free_shipping(self):
        login = LoginPage(self.driver)
        store = StorePage(self.driver)
        cart = CartPage(self.driver)

        # Login & clear
        login.open()
        login.login(VALID_USER['email'], VALID_USER['password'])
        time.sleep(1)
        store.open()
        store.handle_age_verification("01-01-2000")
        time.sleep(1)
        store.open_cart()
        cart.clear_cart()
        time.sleep(1)

        # Add a random product
        store.open()
        time.sleep(1)
        cards = store.get_product_cards()
        valid = [c for c in cards if c.find_elements(By.XPATH, ".//button[contains(@class,'btn-cart')]")]
        assert valid, "No addable product"
        import random
        valid[random.randrange(len(valid))].find_element(By.XPATH, ".//button[contains(@class,'btn-cart')]").click()
        time.sleep(1)

        # increase until free shipping
        store.open_cart()
        plus = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'plus')]")))
        max_tries = 35
        for _ in range(max_tries):
            cost = self.driver.find_element(By.XPATH, "//div[contains(@class,'shipment-container')]/h5[2]").text
            if cost == "0€":
                break
            plus.click()
            time.sleep(1)

        assert cost == "0€", f"Expected free shipping, got {cost}"

    def test_shipping_cost_below_threshold(self):
        login = LoginPage(self.driver)
        store = StorePage(self.driver)
        cart  = CartPage(self.driver)

        # 1) Login + first-time age verification
        login.open()
        login.login(VALID_USER['email'], VALID_USER['password'])
        time.sleep(1)

        store.open()
        store.handle_age_verification("01-01-2000")
        time.sleep(1)

        # 2) Clear the cart
        store.open_cart()
        cart.clear_cart()
        time.sleep(1)

        # 3) Go back to the Store page (no second age check!)
        store.open()
        # Wait until at least one product card is present
        self.wait.until(EC.presence_of_all_elements_located(StorePage.PRODUCT_CARDS))
        time.sleep(1)

        # 4) Add first product to the cart
        store.add_product_to_cart_by_index(0)
        time.sleep(1)

        # 5) Open cart and verify shipping cost is 5€
        store.open_cart()
        time.sleep(1)
        cost = self.driver.find_element(
            By.XPATH, "//div[contains(@class,'shipment-container')]/h5[2]"
        ).text.strip()
        assert cost == "5€", f"Expected shipping cost below threshold to be 5€, but got {cost}"
