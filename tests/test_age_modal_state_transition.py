import pytest
import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from pages.store_page import StorePage


@pytest.mark.usefixtures("driver_init")
class TestAgeModalStateTransition:
    def test_age_modal_reappears_in_new_tab(self):
        store = StorePage(self.driver)
        wait = self.wait

        # Step 1: open shop & verify age
        store.open()
        store.handle_age_verification("01-01-2000")
        time.sleep(1)

        # Step 2: grab alcohol URL
        elem = wait.until(EC.element_to_be_clickable(StorePage.ALCOHOL_LINK))
        url = elem.get_attribute("href")

        # Step 3: open in new tab
        self.driver.execute_script("window.open(arguments[0]);", url)
        time.sleep(1)
        self.driver.switch_to.window(self.driver.window_handles[-1])

        # Step 4: modal should reappear
        try:
            wait.until(EC.visibility_of_element_located(store.AGE_MODAL))
        except TimeoutException:
            pytest.fail("Age modal did not reappear in new tab")
