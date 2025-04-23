import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

@pytest.fixture(scope="function", autouse=True)
def driver_init(request):
    opts = Options()
    opts.add_argument("--incognito")
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    }
    opts.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=opts)
    driver.maximize_window()

    request.cls.driver = driver
    request.cls.wait = WebDriverWait(driver, 10)

    yield
    driver.quit()
