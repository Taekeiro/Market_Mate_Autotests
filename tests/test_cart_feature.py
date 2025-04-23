import pytest
import time
from selenium.webdriver.common.by import By
from pages.login_page import LoginPage
from pages.store_page import StorePage
from pages.cart_page import CartPage
from utils.constants import VALID_USER

@pytest.mark.usefixtures("driver_init")
class TestCartFeature:

    def test_clear_cart(self):
        login = LoginPage(self.driver)
        store = StorePage(self.driver)
        cart  = CartPage(self.driver)

        # 1) Login & Age Verification
        login.open()
        login.login(VALID_USER['email'], VALID_USER['password'])
        time.sleep(1)
        store.open()
        store.handle_age_verification("01-01-2000")
        time.sleep(1)

        # 2) Clear cart
        cart.clear_cart()
        time.sleep(1)

        # 3) Ensure it's empty
        assert cart.get_quantity() == "0"

    def test_add_item_and_verify_quantity(self):
        login = LoginPage(self.driver)
        store = StorePage(self.driver)
        cart  = CartPage(self.driver)

        # 1) Login & age check
        login.open()
        login.login(VALID_USER['email'], VALID_USER['password'])
        time.sleep(1)
        store.open()
        store.handle_age_verification("01-01-2000")
        time.sleep(1)

        # 2) Clear any leftovers
        cart.clear_cart()
        time.sleep(1)

        store.open()
        try:
            store.handle_age_verification("01-01-2000")
        except Exception:
            pass
        time.sleep(1)

        # 3) Add first product to cart
        store.add_product_to_cart_by_index(0)
        time.sleep(1)

        # 4) If redirected to login, log in and retry
        if "/auth" in self.driver.current_url:
            login.open()
            login.login(VALID_USER['email'], VALID_USER['password'])
            time.sleep(1)
            store.click_shop()
            time.sleep(1)
            store.add_product_to_cart_by_index(0)
            time.sleep(1)

        # 5) Open cart and verify quantity is "1"
        cart.open_cart()
        time.sleep(1)
        assert cart.get_quantity() == "1", f"Expected quantity=1, got {cart.get_quantity()}"

    def test_add_multiple_quantities(self):
        login = LoginPage(self.driver)
        store = StorePage(self.driver)
        cart  = CartPage(self.driver)

        # 1) Login & Age Verification
        login.open()
        login.login(VALID_USER['email'], VALID_USER['password'])
        time.sleep(1)

        store.open()
        store.handle_age_verification("01-01-2000")
        time.sleep(1)

        # 2) Clear the cart
        cart.clear_cart()
        time.sleep(1)

        # 3) Return to the Store page (in case clear_cart left us elsewhere)
        store.open()
        try:
            store.handle_age_verification("01-01-2000")
        except Exception:
            pass
        time.sleep(1)

        # 4) On the shop page, pick the first product card
        cards = store.get_product_cards()
        assert cards, "No product cards found"
        first_card = cards[0]

        # 5) Change the quantity input on the card to 5
        qty_input = first_card.find_element(
            By.XPATH, ".//input[@type='number' and contains(@class,'quantity')]"
        )
        qty_input.clear()
        qty_input.send_keys("5")

        # 6) Click the "Add to Cart" button on that same card
        add_btn = first_card.find_element(
            By.XPATH, ".//button[contains(@class,'btn-cart')]"
        )
        add_btn.click()
        time.sleep(1)

        # 7) Open cart and verify quantity is "5"
        cart.open_cart()
        time.sleep(1)
        actual_qty = cart.get_quantity()
        assert actual_qty == "5", f"Expected quantity=5, got {actual_qty}"
