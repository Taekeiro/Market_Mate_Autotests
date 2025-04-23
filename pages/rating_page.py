from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class RatingPage(BasePage):
    REVIEW_WIDGET       = (By.XPATH, "//div[contains(@class,'new-review-card-body')]")
    RESTRICTION_MESSAGE = (By.XPATH, "//div[@class='reviewRestriction']/p")
    ERROR_POPUP         = (By.XPATH,
        "//div[@role='status' and contains(@class,'go3958317564')]")

    def submit_rating(self, stars: int, comment: str):
        # wait for review widget to appear
        self.wait_for_visible(self.REVIEW_WIDGET)
        # click on each star
        for i in range(stars):
            star = self.wait_for_clickable(
                (By.XPATH, f"(//div[contains(@class,'interactive-rating')]/span)[{i+1}]")
            )
            star.click()

        # enter comment
        ta = self.wait_for_visible(
            (By.XPATH, "//textarea[contains(@class,'new-review-form-control')]")
        )
        ta.clear()
        ta.send_keys(comment)

        # click Send
        send = self.wait_for_clickable(
            (By.XPATH, "//button[contains(@class,'new-review-btn-send')]")
        )
        send.click()

    def get_error_popup_text(self) -> str:
        popup = self.wait_for_visible(self.ERROR_POPUP)
        return popup.text.strip()