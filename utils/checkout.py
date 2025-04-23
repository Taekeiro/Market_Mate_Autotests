from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def complete_checkout(driver, wait):
    """
    Completes the checkout process using fake shipping and payment data.

    :param driver: WebDriver instance
    :param wait: WebDriverWait instance
    """
    # Wait for the "Buy now" button to appear
    wait.until(EC.presence_of_element_located(
        (By.XPATH, "//button[contains(@class,'btn-buy-now') and @type='submit']")
    ))

    # Fill in shipment address fields
    driver.find_element(By.NAME, 'street').clear()
    driver.find_element(By.NAME, 'street').send_keys('123 Test Street')
    driver.find_element(By.NAME, 'city').clear()
    driver.find_element(By.NAME, 'city').send_keys('Test City')
    driver.find_element(By.NAME, 'postalCode').clear()
    driver.find_element(By.NAME, 'postalCode').send_keys('12345')

    # Fill in payment details
    driver.find_element(By.NAME, 'cardNumber').clear()
    driver.find_element(By.NAME, 'cardNumber').send_keys('4111111111111111')
    driver.find_element(By.NAME, 'nameOnCard').clear()
    driver.find_element(By.NAME, 'nameOnCard').send_keys('Test User')
    driver.find_element(By.NAME, 'expiration').clear()
    driver.find_element(By.NAME, 'expiration').send_keys('12/2025')  # Format MM/YYYY
    driver.find_element(By.NAME, 'cvv').clear()
    driver.find_element(By.NAME, 'cvv').send_keys('123')

    # Click the "Buy now" button to complete checkout
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(@class,'btn-buy-now') and @type='submit']")
    )).click()