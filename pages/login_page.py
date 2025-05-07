from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.constants import LOGIN_URL


class LoginPage(BasePage):
    # Locators
    EMAIL_INPUT = (By.XPATH, "//input[@type='email']")
    PASSWORD_INPUT = (By.XPATH, "//input[@type='password']")
    SIGNIN_BUTTON = (By.XPATH, "//button[@type='submit' and normalize-space()='Sign In']")

    def open(self):
        """Navigate to the login page, clearing any existing session first."""
        self.driver.delete_all_cookies()
        self.driver.get(LOGIN_URL)

    def login(self, email: str, password: str):
        self.wait_for_visible(self.EMAIL_INPUT).send_keys(email)
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.wait_for_clickable(self.SIGNIN_BUTTON).click()
        # wait until URL changes
        self.wait.until(lambda d: LOGIN_URL not in d.current_url)
