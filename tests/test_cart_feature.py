import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.login_page import LoginPage
from pages.store_page import StorePage
from pages.cart_page import CartPage
from utils.constants import VALID_USER


@pytest.mark.usefixtures("driver_init")
class TestCartFeature:
    def test_clear_cart(self):
        """
        Test Case: Clear the cart.
        Steps:
          1. Open the login page and perform login.
          2. Open the Shop page and handle Age Verification.
          3. Open the Cart page and clear all items.
          4. Verify that the cart is empty.
        Expected Result: Cart is cleared.
        """
        login_page = LoginPage(self.driver)
        cart_page = CartPage(self.driver)
        store_page = StorePage(self.driver)

        # Step 1: Open login page and login
        login_page.open()
        login_page.login(VALID_USER['email'], VALID_USER['password'])
        time.sleep(2)

        # Step 2: Open the Shop page and handle Age Verification
        store_page.open()
        store_page.handle_age_verification("01-01-2000")
        time.sleep(2)

        # Step 3: Open the Cart and clear it
        cart_page.open_cart()
        cart_page.clear_cart()
        time.sleep(2)

        # Step 4: Verify that no quantity input is found (cart is empty)
        try:
            self.driver.find_element(By.XPATH, "//input[contains(@class, 'quantity')]")
            pytest.fail("Cart is not empty after clearing.")
        except Exception:
            print("✅ Cart cleared successfully.")

    def test_add_single_item_to_cart(self):
        """
        Test Case: Add a single item to the cart.
        Steps:
          1. Open the Shop page and handle Age Verification.
          2. Attempt to click "Add to Cart" on the first product.
          3. If the login page appears (URL contains '/auth'), perform login and reattempt.
          4. Open the Cart and verify that the product is added with quantity "1".
        Expected Result: The cart shows 1 product.
        """
        login_page = LoginPage(self.driver)
        store_page = StorePage(self.driver)
        cart_page = CartPage(self.driver)

        # Step 1: Open the Shop page and handle Age Verification
        store_page.open()
        store_page.handle_age_verification("01-01-2000")
        time.sleep(2)

        # Step 2: Get the list of product cards and click the "Add to Cart" button of the first product
        products = self.wait.until(EC.presence_of_all_elements_located(store_page.product_cards))
        assert len(products) > 0, "No product cards found on the store page."
        product_card = products[0]
        try:
            add_to_cart_button = product_card.find_element(By.XPATH, ".//button[contains(@class, 'btn-cart')]")
        except Exception:
            pytest.fail("Add to Cart button not found in the first product card.")
        add_to_cart_button.click()
        time.sleep(2)

        # Step 3: If the login page appears, perform login and retry adding the item.
        if "/auth" in self.driver.current_url:
            print("Auth page detected, performing login.")
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']")))
            login_page.login(VALID_USER['email'], VALID_USER['password'])
            time.sleep(2)
            # After login, click the "Shop" link on the homepage to return to the Store page.
            try:
                shop_link = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Shop']")))
                shop_link.click()
            except Exception:
                pytest.fail("Shop link not found on homepage after login.")
            time.sleep(2)
            # Retry adding the item:
            products = self.wait.until(EC.presence_of_all_elements_located(store_page.product_cards))
            assert len(products) > 0, "No product cards found after login."
            product_card = products[0]
            add_to_cart_button = product_card.find_element(By.XPATH, ".//button[contains(@class, 'btn-cart')]")
            add_to_cart_button.click()
            time.sleep(2)

        # Step 4: Open the Cart and verify product quantity is "1"
        cart_page.open_cart()
        quantity = cart_page.get_quantity()
        assert quantity == "1", f"Expected product quantity to be 1, but found {quantity}"
        print("✅ Product successfully added to cart with quantity 1.")

    def test_add_multiple_quantities(self):
        """
        Test Case: Add multiple quantities of the same item.
        Steps:
          1. Open the login page and log in.
          2. Open the Shop page and handle Age Verification.
          3. Open the Cart and clear any existing items.
          4. Reopen the Shop page (and handle Age Verification if necessary).
          5. Open a product page by clicking on the first product's link.
          6. Update the quantity input field to "5" and click "Add to Cart".
          7. Open the Cart and verify that the product quantity is "5".
        Expected Result: The cart shows 5 items.
        """
        login_page = LoginPage(self.driver)
        store_page = StorePage(self.driver)
        cart_page = CartPage(self.driver)

        # Step 1: Open login page and perform login.
        login_page.open()
        login_page.login(VALID_USER['email'], VALID_USER['password'])
        time.sleep(2)

        # Step 2: Open the Shop page and handle Age Verification.
        store_page.open()
        store_page.handle_age_verification("01-01-2000")
        time.sleep(2)

        # Step 3: Open the Cart and clear it.
        cart_page.open_cart()
        cart_page.clear_cart()
        time.sleep(2)

        # Step 4: Reopen the Shop page and handle Age Verification if needed.
        store_page.open()
        try:
            self.wait.until(EC.visibility_of_element_located(store_page.age_modal), timeout=5)
            store_page.handle_age_verification("01-01-2000")
        except Exception:
            print("Age verification modal not present upon reopening; proceeding.")
        time.sleep(2)

        # Step 5: Open product page by clicking the first product's link.
        product_cards = store_page.get_product_cards()
        assert len(product_cards) > 0, "No product cards found on the Store page."
        product_card = product_cards[0]
        product_link = product_card.find_element(By.XPATH, ".//a")
        product_link.click()
        time.sleep(2)

        # Step 6: Update the quantity input to "5" and click "Add to Cart".
        try:
            quantity_input = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//input[@type='number' and contains(@class, 'quantity')]")
            ))
            quantity_input.clear()
            quantity_input.send_keys("5")
        except TimeoutException:
            pytest.fail("Quantity input field not found on the product page.")
        try:
            add_to_cart_button = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class, 'btn-cart') and contains(text(), 'Add to Cart')]")
            ))
            add_to_cart_button.click()
        except TimeoutException:
            pytest.fail("Add to Cart button not clickable on product page.")
        time.sleep(2)

        # Step 7: Open the Cart and verify that the product quantity is "5".
        cart_page.open_cart()
        time.sleep(2)
        cart_quantity = cart_page.get_quantity()
        assert cart_quantity == "5", f"Expected product quantity to be 5, but found {cart_quantity}"
        print("✅ Cart reflects 5 items.")
