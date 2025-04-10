from selenium.webdriver.common.by import By


class RatingPage:
    def __init__(self, driver):
        self.driver = driver
        # For submitting a rating
        self.five_star = (By.XPATH, "(//div[contains(@class, 'interactive-rating')]/span)[5]")
        self.new_review_textarea = (By.XPATH, "//textarea[contains(@class, 'new-review-form-control')]")
        self.send_button = (By.XPATH, "//button[contains(@class, 'new-review-btn-send')]")
        # For dropdown actions (edit and delete)
        self.menu_icon = (By.XPATH, "//div[@class='menu-icon']")
        self.dropdown_edit = (By.XPATH, "//div[@class='dropdown-menu']//button[normalize-space()='Edit']")
        self.dropdown_delete = (By.XPATH, "//div[@class='dropdown-menu']//button[normalize-space()='Delete']")

    def submit_rating(self, rating, comment):
        if rating == 5:
            self.driver.find_element(*self.five_star).click()
        self.driver.find_element(*self.new_review_textarea).clear()
        self.driver.find_element(*self.new_review_textarea).send_keys(comment)
        self.driver.find_element(*self.send_button).click()
