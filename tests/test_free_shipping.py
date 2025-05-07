import pytest

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

        store.open()
        store.handle_age_verification("01-01-2000")

        cart.open_cart()
        cart.clear_cart()

        store.open()

        store.add_product_to_cart_by_index(0)
        cart.open_cart()

        # click + until free shipping applies
        for _ in range(35):
            cost = cart.get_shipping_cost()
            if cost == "0€":
                break
            cart.click_plus_button()

        assert cart.get_shipping_cost() == "0€"

    def test_shipping_cost_below_threshold(self):
        login = LoginPage(self.driver)
        store = StorePage(self.driver)
        cart  = CartPage(self.driver)

        login.open()
        login.login(VALID_USER['email'], VALID_USER['password'])

        store.open()
        store.handle_age_verification("01-01-2000")

        cart.open_cart()
        cart.clear_cart()

        store.open()

        store.add_product_to_cart_by_index(0)
        cart.open_cart()

        assert cart.get_shipping_cost() == "5€"
