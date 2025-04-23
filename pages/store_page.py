from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage


class StorePage(BasePage):
    URL               = "https://grocerymate.masterschool.com/store"
    AGE_MODAL         = (By.XPATH, "//div[@class='modal-content']")
    AGE_INPUT         = (By.XPATH, "//input[@placeholder='DD-MM-YYYY']")
    AGE_CONFIRM_BTN   = (By.XPATH, "//div[@class='modal-content']//button[normalize-space()='Confirm']")
    PRODUCT_CARDS     = (By.XPATH, "//div[contains(@class,'product-card')]")
    ADD_TO_CART_BTN = (By.XPATH,
                       ".//button[contains(@class,'btn-cart') and normalize-space()='Add to Cart']")
    SHOP_LINK         = (By.XPATH, "//a[normalize-space()='Shop']")
    CART_ICON = (By.XPATH,
                 "(//div[@class='social-icon-cont']//div[contains(@class,'headerIcon')])[3]")
    ALCOHOL_LINK = (By.XPATH,
                    "//div[contains(@class,'widget widget-menu')]//ul/li/a[normalize-space()='Alocohol']")

    def open(self):
        """Navigate to the store page."""
        self.driver.get(self.URL)

    def handle_age_verification(self, birth_date: str):
        self.wait_for_visible(self.AGE_MODAL)
        self.driver.find_element(*self.AGE_INPUT).send_keys(birth_date)
        self.driver.find_element(*self.AGE_CONFIRM_BTN).click()
        self.wait_for_invisible(self.AGE_MODAL)

    def get_product_cards(self):
        return self.wait.until(lambda d: d.find_elements(*self.PRODUCT_CARDS))

    def add_product_to_cart_by_index(self, index: int):
        locator = (
            By.XPATH,
            f"(//div[contains(@class,'product-card')])[{index + 1}]"
            f"//button[contains(@class,'btn-cart') and normalize-space()='Add to Cart']"
        )
        self.wait_for_clickable(locator).click()

    def open_product_by_index(self, index: int):
        """
        Scrolls to and clicks the product at given zero-based index,
        by clicking its <img> or <p class='lead'> element.
        """
        # 1) wait until cards loaded
        cards = self.wait.until(lambda d: d.find_elements(*self.PRODUCT_CARDS))
        if index >= len(cards):
            raise IndexError(f"Requested index {index} but only {len(cards)} cards available")
        # 2) Build locator for a clickable child element.
        xpath = (
            f"(//div[contains(@class,'product-card')])[{index+1}]"
            "//img | "
            f"(//div[contains(@class,'product-card')])[{index+1}]"
            "//p[@class='lead']"
        )
        locator = (By.XPATH, xpath)
        # 3) wait until clickable
        elem = self.wait_for_clickable(locator)
        # 4) scroll and press
        self.driver.execute_script("arguments[0].scrollIntoView(true);", elem)
        elem.click()

    def click_shop(self):
        self.wait_for_clickable(self.SHOP_LINK).click()

    def open_cart(self):
        self.wait_for_clickable(self.CART_ICON).click()

    def open_alcohol_section(self):
        self.wait_for_clickable(self.ALCOHOL_LINK).click()

    def open_alcohol_in_new_tab(self):
        link = self.wait_for_clickable(self.ALCOHOL_LINK)
        link.send_keys(Keys.CONTROL + Keys.RETURN)

    def set_product_quantity_by_index(self, index: int, quantity: int):
        """
        Sets the quantity input on the product card at `index` to `quantity`.
        Uses an explicit wait for the specific input element.
        """
        locator = (
            By.XPATH,
            f"(//div[contains(@class,'product-card')])[{index+1}]"
            "//input[@type='number' and contains(@class,'quantity')]"
        )
        # waiting for  input to appear
        inp = self.wait.until(lambda d: d.find_element(*locator))
        inp.clear()
        inp.send_keys(str(quantity))
