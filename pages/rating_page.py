from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class RatingPage(BasePage):
    """Page object for submitting, editing and deleting product reviews."""

    # --- Locators ---
    REVIEW_WIDGET        = (By.XPATH, "//div[contains(@class,'new-review-card-body')]")
    ERROR_POPUP          = (By.XPATH, "//div[@role='status' and contains(@class,'go3958317564')]")
    RATING_STARS         = (By.XPATH, "//div[contains(@class,'interactive-rating')]/span")
    COMMENT_TEXTAREA     = (By.CSS_SELECTOR, "textarea.new-review-form-control")
    SEND_BUTTON          = (By.CSS_SELECTOR, "button.new-review-btn-send")
    RESTRICTION_MESSAGE  = (By.CSS_SELECTOR, "div.reviewRestriction > p")
    EDIT_DROPDOWN_BTN    = (By.CSS_SELECTOR, "div.menu-icon")
    EDIT_BUTTON          = (By.XPATH, "//div[@class='dropdown-menu']//button[normalize-space()='Edit']")
    DELETE_BUTTON        = (By.XPATH, "//div[@class='dropdown-menu']//button[normalize-space()='Delete']")
    MODAL_RATING_INPUT   = (By.XPATH, "//div[@class='modal']//label[contains(.,'Rating')]/input")
    MODAL_COMMENT_INPUT  = (By.XPATH, "//div[@class='modal']//label[contains(.,'Comment')]/textarea")
    MODAL_SAVE_BTN       = (By.XPATH, "//button[normalize-space()='Save Changes']")
    NEW_REVIEW_FORM      = (By.CSS_SELECTOR, "div.new-review-card-body")

    def submit_rating(self, stars: int, comment: str):
        """
        Click the nth star (1-based, 0 = none), enter comment, then click Send.
        """
        stars_elems = self.wait_for_visible_all(self.RATING_STARS)
        if 1 <= stars <= len(stars_elems):
            stars_elems[stars-1].click()
        textarea = self.wait_for_visible(self.COMMENT_TEXTAREA)
        textarea.clear()
        textarea.send_keys(comment)
        self.wait_for_clickable(self.SEND_BUTTON).click()

    def wait_for_restriction(self, timeout: int = 5):
        """
        Wait until the “You need to buy this product…” message appears.
        """
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.RESTRICTION_MESSAGE)
        )

    def edit_rating(self, new_stars: int, new_comment: str):
        """
        Open dropdown → Edit → update stars & comment → Save Changes.
        """
        self.wait_for_clickable(self.EDIT_DROPDOWN_BTN).click()
        self.wait_for_clickable(self.EDIT_BUTTON).click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.MODAL_RATING_INPUT)
        )
        inp = self.driver.find_element(*self.MODAL_RATING_INPUT)
        inp.clear()
        inp.send_keys(str(new_stars))
        ta = self.driver.find_element(*self.MODAL_COMMENT_INPUT)
        ta.clear()
        ta.send_keys(new_comment)
        self.wait_for_clickable(self.MODAL_SAVE_BTN).click()
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located(self.MODAL_SAVE_BTN)
        )

    def delete_rating(self):
        """
        Open dropdown → Delete → accept browser alert.
        """
        self.wait_for_clickable(self.EDIT_DROPDOWN_BTN).click()
        self.wait_for_clickable(self.DELETE_BUTTON).click()
        alert = WebDriverWait(self.driver, 10).until(lambda d: d.switch_to.alert)
        alert.accept()
        # wait until the review form reappears
        self.wait_for_new_review_form()

    def wait_for_new_review_form(self, timeout: int = 5):
        """
        Wait until the “Add a comment” form is visible,
        indicating the previous review was deleted.
        """
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.NEW_REVIEW_FORM)
        )

    def get_error_popup_text(self) -> str:
        popup = self.wait_for_visible(self.ERROR_POPUP)
        return popup.text.strip()
