import pytest
from pages.store_page import StorePage


@pytest.mark.usefixtures("driver_init")
class TestAgeModalStateTransition:

    def test_age_modal_reappears_in_new_tab(self):
        store = StorePage(self.driver)
        store.open()
        store.handle_age_verification("01-01-2000")

        # open Alcohol in new tab
        store.open_alcohol_in_new_tab()
        # switch to the new tab
        self.driver.switch_to.window(self.driver.window_handles[-1])

        # modal must reappear
        store.wait_for_visible(StorePage.AGE_MODAL)