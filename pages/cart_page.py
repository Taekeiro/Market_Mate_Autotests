# pages/cart_page.py
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CartPage:
    CART_ICON      = (By.XPATH, "(//div[@class='social-icon-cont']//div[contains(@class,'headerIcon')])[3]")
    REMOVE_ICON    = (By.XPATH, "//a[@class='remove-icon']")
    QUANTITY_INPUT = (By.XPATH, "//input[contains(@class,'quantity')]")

    def __init__(self, driver):
        self.driver = driver
        self.wait   = WebDriverWait(driver, 10)

    def open_cart(self):
        """Клик по иконке корзины."""
        self.driver.find_element(*self.CART_ICON).click()

    def clear_cart(self):
        """
        delete all products from cart
        """
        self.open_cart()
        time.sleep(1)
        while True:
            try:
                remove = self.wait.until(EC.element_to_be_clickable(self.REMOVE_ICON))
                remove.click()
                time.sleep(0.5)
            except Exception:
                break

    def get_quantity(self):
        """
        Возвращает текущее значение в поле quantity.
        Если поле не найдено, значит корзина пуста — возвращаем "0".
        """
        try:
            elem = self.driver.find_element(*self.QUANTITY_INPUT)
            return elem.get_attribute("value")
        except NoSuchElementException:
            return "0"
