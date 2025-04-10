from selenium.webdriver.common.by import By
from utils.constants import LOGIN_URL


class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.email_input = (By.XPATH, "//input[@type='email']")
        self.password_input = (By.XPATH, "//input[@type='password']")
        self.login_button = (By.XPATH, "//button[@type='submit' and contains(., 'Sign In')]")

    def open(self):
        self.driver.get(LOGIN_URL)
        self.wait_for_page_load()

    def wait_for_page_load(self, timeout=15):
        from selenium.webdriver.support.ui import WebDriverWait
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    def login(self, email, password):
        self.driver.find_element(*self.email_input).send_keys(email)
        self.driver.find_element(*self.password_input).send_keys(password)
        self.driver.find_element(*self.login_button).click()
