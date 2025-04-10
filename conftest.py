import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait


@pytest.fixture(scope="function")
def driver_init(request):
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    }
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    request.cls.driver = driver
    # Use a wait timeout of 15 seconds
    request.cls.wait = WebDriverWait(driver, 15)
    yield
    driver.quit()
