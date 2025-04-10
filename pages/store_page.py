from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from utils.constants import PRODUCT_PAGE_URL


class StorePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
        self.url = PRODUCT_PAGE_URL
        self.age_modal = (By.XPATH, "//div[@class='modal-content']")
        self.date_input = (By.XPATH, "//input[@placeholder='DD-MM-YYYY']")
        self.confirm_btn = (By.XPATH, "//div[@class='modal-content']//button[normalize-space()='Confirm']")
        self.product_cards = (By.XPATH, "//div[contains(@class, 'product-card')]")
        self.shop_link = (By.XPATH, "//a[normalize-space()='Shop']")
        # Note: Using the text "Alocohol" as specified
        self.alcohol_link = (By.XPATH, "//div[contains(@class, 'widget widget-menu')]//ul/li/a[normalize-space()='Alocohol']")

    def wait_for_page_load(self, timeout=15):
        self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

    def open(self):
        self.driver.get(self.url)
        self.wait_for_page_load()

    def handle_age_verification(self, birth_date="01-01-2000"):
        self.wait_for_page_load()
        modal = self.driver.find_element(*self.age_modal)
        date_input = self.driver.find_element(*self.date_input)
        date_input.clear()
        date_input.send_keys(birth_date)
        self.driver.find_element(*self.confirm_btn).click()
        # Wait for modal to vanish
        self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

    def get_product_cards(self):
        self.wait_for_page_load()
        return self.driver.find_elements(*self.product_cards)
