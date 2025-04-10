import random
import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.store_page import StorePage
from pages.cart_page import CartPage
from utils.constants import VALID_USER


@pytest.mark.usefixtures("driver_init")
class TestFreeShipping:
    def test_free_shipping(self):
        driver = self.driver
        wait = self.wait

        # Create page objects
        login_page = LoginPage(driver)
        store_page = StorePage(driver)
        cart_page = CartPage(driver)

        # Step 1: Log in to the site
        login_page.open()
        login_page.login(VALID_USER['email'], VALID_USER['password'])
        time.sleep(2)

        # Step 2: Open the Store page and handle Age Verification
        store_page.open()
        store_page.handle_age_verification("01-01-2000")
        time.sleep(2)

        # Step 3: Open the Cart and clear any existing items
        cart_page.open_cart()
        cart_page.clear_cart()
        time.sleep(2)

        # Step 4: Reopen the Store page and handle Age Verification if needed
        store_page.open()
        try:
            # Wait up to 5 seconds for the age modal to appear
            wait.until(EC.visibility_of_element_located(store_page.age_modal), timeout=5)
            store_page.handle_age_verification("01-01-2000")
        except Exception:
            print("Age verification modal not present; proceeding.")
        time.sleep(2)

        # Step 5: Randomly select a product with an "Add to Cart" button and add it to the cart
        product_cards = store_page.get_product_cards()
        if not product_cards:
            pytest.fail("No product cards found on the store page.")
        valid_cards = [card for card in product_cards if
                       card.find_elements(By.XPATH, ".//button[contains(@class, 'btn-cart')]")]
        if not valid_cards:
            pytest.fail("No product card with an 'Add to Cart' button found.")
        random_product = random.choice(valid_cards)
        add_to_cart_button = random_product.find_element(By.XPATH, ".//button[contains(@class, 'btn-cart')]")
        add_to_cart_button.click()
        time.sleep(2)

        # Step 6: Open the Cart page
        cart_page.open_cart()
        time.sleep(2)

        # Step 7: Click the plus button repeatedly until the shipping cost becomes "0€"
        max_attempts = 40
        attempt = 0
        while attempt < max_attempts:
            current_shipping = cart_page.get_shipment_cost()
            if current_shipping == "0€":
                break
            try:
                # Locate the plus button using its class 'plus'
                plus_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='plus']")))
            except Exception:
                pytest.fail("Plus button not found on the Cart page.")
            plus_button.click()
            time.sleep(1)
            attempt += 1

        final_shipping = cart_page.get_shipment_cost()
        assert final_shipping == "0€", f"Expected free shipping with cost '0€', but got {final_shipping}"
        print("✅ Free shipping applied: shipping cost is 0€")
