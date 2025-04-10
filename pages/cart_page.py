from selenium.webdriver.common.by import By
import time


class CartPage:
    def __init__(self, driver):
        self.driver = driver
        self.cart_icon = (By.XPATH, "(//div[@class='social-icon-cont']//div[contains(@class, 'headerIcon')])[3]")
        self.remove_icon = (By.XPATH, "//a[@class='remove-icon']")
        self.quantity_input = (By.XPATH, "//input[contains(@class, 'quantity')]")
        self.shipment_cost = (By.XPATH, "//div[contains(@class, 'shipment-container')]/h5[2]")

    def open_cart(self):
        self.driver.find_element(*self.cart_icon).click()
        time.sleep(2)

    def clear_cart(self):
        while True:
            try:
                self.driver.find_element(*self.remove_icon).click()
                time.sleep(1)
            except Exception:
                break
        self.driver.refresh()
        time.sleep(2)

    def get_quantity(self):
        return self.driver.find_element(*self.quantity_input).get_attribute("value")

    def get_shipment_cost(self):
        return self.driver.find_element(*self.shipment_cost).text.strip()
