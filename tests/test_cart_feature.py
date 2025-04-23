import pytest
from selenium.common.exceptions import TimeoutException

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

        login.open()
        login.login(VALID_USER['email'], VALID_USER['password'])

        store.open()
        store.handle_age_verification("01-01-2000")

        cart.open_cart()
        cart.clear_cart()

        # cart should be empty: no quantity input visible
        with pytest.raises(TimeoutException):
            cart.wait_for_visible(CartPage.QUANTITY_INPUT)

    def test_add_item_and_verify_quantity(self):
        login = LoginPage(self.driver)
        store = StorePage(self.driver)
        cart  = CartPage(self.driver)

        login.open()
        login.login(VALID_USER['email'], VALID_USER['password'])

        store.open()
        store.handle_age_verification("01-01-2000")

        # wait for products then add first one
        store.wait_for_visible(StorePage.PRODUCT_CARDS)
        store.add_product_to_cart_by_index(0)

        cart.open_cart()
        qty = cart.get_quantity()
        assert qty == "1", f"Expected 1 item, found {qty}"

    def test_add_multiple_quantities(self):
        login = LoginPage(self.driver)
        store = StorePage(self.driver)
        cart  = CartPage(self.driver)

        # 1) Login + age-verification
        login.open()
        login.login(VALID_USER['email'], VALID_USER['password'])
        store.open()
        store.handle_age_verification("01-01-2000")

        # 2) Clear cart
        cart.open_cart()
        cart.clear_cart()

        # 3) Go back to shop
        store.open()

        # 4) On product #1 set quantity to 5, click Add to Cart
        store.set_product_quantity_by_index(0, 5)
        store.add_product_to_cart_by_index(0)

        # 5) WAIT for toast to disappear before opening cart
        store.wait_for_toast_disappear()

        # 6) Open cart and wait for quantity-input to appear
        cart.open_cart()
        qty_elem = cart.wait_for_visible(CartPage.QUANTITY_INPUT)
        qty = qty_elem.get_attribute("value")

        # 7) Final assertion
        assert qty == "5", f"Expected 5 items, found {qty}"
