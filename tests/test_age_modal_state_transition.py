import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.store_page import StorePage


@pytest.mark.usefixtures("driver_init")
class TestAgeModalStateTransition:
    def test_age_modal_reappearance_in_new_tab(self):
        """
        Test Case: Reappearance of the age verification modal in a new tab.
        Steps:
          - Access the alcohol section and confirm age.
          - Open the alcohol section URL in a new browser tab.
        Expected Result: The age verification modal reappears in the new tab, requiring the user to re-enter their age.
        """
        # Create a StorePage object.
        store_page = StorePage(self.driver)
        wait = self.wait

        # Step 1: Open the Store page and handle Age Verification.
        store_page.open()
        store_page.handle_age_verification("01-01-2000")
        time.sleep(2)

        # Step 2: Find the Alcohol link in the left menu.
        try:
            alcohol_link_element = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(@class, 'widget widget-menu')]//ul/li/a[normalize-space()='Alocohol']")
            ))
        except TimeoutException:
            pytest.fail("Alcohol link not found on the Store page.")

        # Get the href attribute of the alcohol link.
        alcohol_url = alcohol_link_element.get_attribute("href")
        if not alcohol_url:
            pytest.fail("Alcohol link does not have a valid URL.")

        # Step 3: Open the Alcohol URL in a new browser tab.
        self.driver.execute_script("window.open(arguments[0]);", alcohol_url)
        time.sleep(2)
        # Switch to the new tab (the last handle)
        window_handles = self.driver.window_handles
        self.driver.switch_to.window(window_handles[-1])
        time.sleep(2)

        # Step 4: Verify that the age verification modal appears in the new tab.
        try:
            modal = wait.until(EC.visibility_of_element_located(store_page.age_modal))
            print("✅ Age verification modal reappeared in the new tab.")
        except TimeoutException:
            pytest.fail("❌ Age verification modal did not reappear in the new tab.")
