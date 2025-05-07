from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """Base for all page-objects: holds driver and WebDriverWait."""
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait   = WebDriverWait(driver, timeout)

    def wait_for_visible(self, locator, timeout: int = None):
        return (WebDriverWait(self.driver, timeout or self.wait._timeout)
                .until(EC.visibility_of_element_located(locator)))

    def wait_for_visible_all(self, locator, timeout: int = None):
        return (WebDriverWait(self.driver, timeout or self.wait._timeout)
                .until(EC.visibility_of_all_elements_located(locator)))

    def wait_for_clickable(self, locator, timeout: int = None):
        return (WebDriverWait(self.driver, timeout or self.wait._timeout)
                .until(EC.element_to_be_clickable(locator)))

    def wait_for_invisible(self, locator):
        return self.wait.until(EC.invisibility_of_element_located(locator))

    def wait_for_toast_disappear(self, timeout: int = None):
        TOAST = (By.CSS_SELECTOR, "div[role='status'].go3958317564")
        try:
            WebDriverWait(self.driver, timeout or self.wait._timeout)\
                .until(EC.invisibility_of_element_located(TOAST))
        except:
            pass
