import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="function")
def driver_init(request):
    opts = Options()
    prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False}
    opts.add_experimental_option("prefs", prefs)
    opts.add_argument("--incognito")
    driver = webdriver.Chrome(options=opts)
    driver.maximize_window()
    request.cls.driver = driver
    yield driver
    driver.quit()
