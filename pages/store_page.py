from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class StorePage:
    URL               = "https://grocerymate.masterschool.com/store"
    AGE_MODAL         = (By.XPATH, "//div[@class='modal-content']")
    AGE_INPUT         = (By.XPATH, "//input[@placeholder='DD-MM-YYYY']")
    AGE_CONFIRM_BTN   = (By.XPATH, "//div[@class='modal-content']//button[normalize-space()='Confirm']")
    PRODUCT_CARDS     = (By.XPATH, "//div[contains(@class,'product-card')]")
    ADD_TO_CART_BTN   = (By.XPATH, ".//button[contains(@class,'btn-cart')]")
    SHOP_LINK         = (By.XPATH, "//a[normalize-space()='Shop']")
    CART_ICON         = (By.XPATH, "(//div[@class='social-icon-cont']//div[contains(@class,'headerIcon')])[3]")
    ALCOHOL_LINK      = (By.XPATH, "//div[contains(@class,'widget widget-menu')]//ul/li/a[normalize-space()='Alocohol']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        """Navigate to the store page."""
        self.driver.get(self.URL)

    def handle_age_verification(self, birth_date: str):
        """Enter birth date and confirm age verification."""
        self.wait.until(EC.visibility_of_element_located(self.AGE_MODAL))
        self.driver.find_element(*self.AGE_INPUT).send_keys(birth_date)
        self.driver.find_element(*self.AGE_CONFIRM_BTN).click()
        self.wait.until(EC.invisibility_of_element_located(self.AGE_MODAL))

    def open_alcohol_section(self):
        """Click the Alcohol link in the left‑hand menu."""
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.ALCOHOL_LINK)
        ).click()

    def open_alcohol_in_new_tab(self):
        """Open the Alcohol link in a new tab (Ctrl+Enter)."""
        link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.ALCOHOL_LINK)
        )
        link.send_keys(Keys.CONTROL + Keys.RETURN)

    def get_product_cards(self):
        """Return list of all product card elements."""
        return self.wait.until(EC.presence_of_all_elements_located(self.PRODUCT_CARDS))

    def add_product_to_cart_by_index(self, index: int):
        """
        Click the Add to Cart button for the product at zero-based index.
        Uses an absolute XPath to avoid stale/relative issues.
        """
        locator = (
            By.XPATH,
            f"(//div[contains(@class,'product-card')])[{index+1}]"
            f"//button[contains(@class,'btn-cart') and normalize-space()='Add to Cart']"
        )
        # wait until that exact button is clickable, then click it
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def open_product_by_index(self, index: int):
        """
        Click on the product card at the given zero-based index.
        Waits for cards to be present, then scrolls into view and clicks.
        """
        # wait for at least (index+1) cards to be present
        cards = self.wait.until(EC.presence_of_all_elements_located(self.PRODUCT_CARDS))
        if index >= len(cards):
            raise IndexError(f"Requested product index {index} but only {len(cards)} cards found.")
        card = cards[index]
        # scroll the card into view
        self.driver.execute_script("arguments[0].scrollIntoView(true);", card)
        # wait until this card is clickable (visible & enabled)
        self.wait.until(lambda d: card.is_displayed() and card.is_enabled())
        card.click()

    def click_shop(self):
        """Click the Shop link in the header to return to store page."""
        self.wait.until(EC.element_to_be_clickable(self.SHOP_LINK)).click()

    def open_cart(self):
        """Click the cart icon to open the cart."""
        self.wait.until(EC.element_to_be_clickable(self.CART_ICON)).click()


