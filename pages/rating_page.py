from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RatingPage:
    REVIEW_WIDGET       = (By.XPATH, "//div[contains(@class,'new-review-card-body')]")
    RESTRICTION_MESSAGE = (By.XPATH, "//div[@class='reviewRestriction']/p")
    ERROR_POPUP         = (By.XPATH, "//div[@role='status' and contains(@class,'go3958317564')]")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def submit_rating(self, stars: int, comment: str):
        """Select stars, enter comment, and click Send."""
        self.wait.until(EC.visibility_of_element_located(self.REVIEW_WIDGET))
        # click stars
        for i in range(stars):
            star = self.driver.find_element(
                By.XPATH,
                f"(//div[contains(@class,'interactive-rating')]/span)[{i+1}]"
            )
            star.click()
        # enter comment
        textarea = self.driver.find_element(
            By.XPATH, "//textarea[contains(@class,'new-review-form-control')]"
        )
        textarea.clear()
        textarea.send_keys(comment)
        # click Send
        send_button = self.driver.find_element(
            By.XPATH, "//button[contains(@class,'new-review-btn-send')]"
        )
        send_button.click()

    def get_error_popup_text(self) -> str:
        """Wait for error popup and return its text."""
        popup = self.wait.until(EC.visibility_of_element_located(self.ERROR_POPUP))
        return popup.text.strip()
