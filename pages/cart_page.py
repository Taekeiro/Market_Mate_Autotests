from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class CartPage(BasePage):
    """Page object for the shopping cart."""

    # --- Locators ---
    CART_ICON      = (By.XPATH, "(//div[@class='social-icon-cont']//div[contains(@class,'headerIcon')])[3]")
    QUANTITY_INPUT = (By.XPATH, "//input[contains(@class,'quantity')]")
    REMOVE_ICON    = (By.XPATH, "//a[@class='remove-icon']")
    REMOVE_BTN     = (By.XPATH, "//button[normalize-space()='Remove']")
    PLUS_BUTTON    = (By.XPATH, "//button[contains(@class,'plus')]")
    SHIPPING_COST  = (By.XPATH, "//div[contains(@class,'shipment-container')]/h5[2]")

    # --- Actions ---
    def open_cart(self):
        """Click the cart icon in the header to open the cart."""
        self.wait_for_clickable(self.CART_ICON).click()

    def clear_cart(self):
        """
        Remove all items from the cart by:
        1) Clicking the '×' icon until none remain;
        2) Clicking any 'Remove' buttons until none remain;
        3) Waiting until no quantity-input fields are visible.
        """
        # 1) Remove via '×' icons
        while True:
            icons = self.driver.find_elements(*self.REMOVE_ICON)
            if not icons:
                break
            # click the first remove-icon
            icons[0].click()
            # wait until that icon disappears
            self.wait.until(lambda d: len(d.find_elements(*self.REMOVE_ICON)) < len(icons))

        # 2) Remove via "Remove" buttons
        while True:
            buttons = self.driver.find_elements(*self.REMOVE_BTN)
            if not buttons:
                break
            buttons[0].click()
            # wait until that button is stale/removed
            self.wait.until(EC.staleness_of(buttons[0]))

        # 3) Ensure no quantity inputs remain
        self.wait.until(lambda d: not d.find_elements(*self.QUANTITY_INPUT))

    def get_quantity(self) -> str:
        """
        Return the quantity value of the first item in the cart.
        """
        elem = self.wait.until(lambda d: d.find_element(*self.QUANTITY_INPUT))
        return elem.get_attribute("value")

    def click_plus_button(self):
        """Click the “+” button to increase the item quantity by one."""
        self.wait_for_clickable(self.PLUS_BUTTON).click()

    def get_shipping_cost(self) -> str:
        """Return the displayed shipping cost (e.g. "0€" or "5€")."""
        elem = self.wait_for_visible(self.SHIPPING_COST)
        return elem.text.strip()
