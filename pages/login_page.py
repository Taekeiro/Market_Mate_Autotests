from selenium.webdriver.common.by import By

class LoginPage:
    # Locators
    LOGIN_URL = "https://grocerymate.masterschool.com/auth"
    EMAIL_INPUT = (By.XPATH, "//input[@type='email']")
    PASSWORD_INPUT = (By.XPATH, "//input[@type='password']")
    SIGN_IN_BUTTON = (By.XPATH, "//button[@type='submit' and normalize-space()='Sign In']")

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        """Navigate to the login page, clearing any existing session first."""
        self.driver.delete_all_cookies()
        self.driver.get(self.LOGIN_URL)

    def login(self, email: str, password: str):
        """
        Perform login using provided credentials.
        :param email: user email
        :param password: user password
        """
        self.driver.find_element(*self.EMAIL_INPUT).send_keys(email)
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*self.SIGN_IN_BUTTON).click()