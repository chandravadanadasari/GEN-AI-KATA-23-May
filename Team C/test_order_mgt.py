# test_create_order.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import pytest

# Update this URL to the page where your form is located.
FORM_URL = 'http://localhost:8000/create-order'


@pytest.fixture
def driver():
    # Here you can use the appropriate WebDriver (e.g., Chrome, Firefox, etc.)
    with webdriver.Chrome(executable_path="path/to/chromedriver") as browser:
        browser.get(FORM_URL)
        yield browser


def test_create_new_order(driver):
    # Select the Supplier Name
    Select(driver.find_element(By.ID, 'supplierName')).select_by_visible_text('Supplier A')

    # Automatically populated fields (assumed to be filled)
    order_id = driver.find_element(By.ID, 'orderId').get_attribute('value')
    assert order_id, "Order ID should be automatically populated"

    # Enter a product and quantity
    Select(driver.find_element(By.ID, 'product')).select_by_visible_text('Product A')
    quantity_field = driver.find_element(By.ID, 'quantity')
    quantity_field.clear()
    quantity_field.send_keys('10')

    # Assuming Unit Price gets populated based on product selection, let's check it
    unit_price = driver.find_element(By.ID, 'unitPrice').get_attribute('value')
    assert float(unit_price) > 0, "Unit price should be automatically populated and greater than zero"

    # Add Product to the order
    driver.find_element(By.ID, 'addProduct').click()

    # Assuming the delivery options get populated, let's choose an option
    Select(driver.find_element(By.ID, 'deliveryOptions')).select_by_visible_text('Free, 10 day')

    # Set some comments
    comments_area = driver.find_element(By.ID, 'comments')
    comments_area.clear()
    comments_area.send_keys('Order placed by automated test.')

    # Save the order
    driver.find_element(By.XPATH, '//button[text()="Save"]').click()

    # Verify if the order was saved successfully
    # This is highly dependent on how your application gives feedback.
    # Here we'll just search for an element by a hypothetical success message.

    # Commented out because the success element ID or class will vary based on the actual application
    # success_message = driver.find_element(By.ID, 'success-id')
    # assert success_message, "The success message should be displayed after saving"


# Code to run the script if this file is executed directly
def test_order_list_display(driver):
    order_list = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#orderList > .orderRow"))
    )
    assert len(order_list) > 0, "The order list should display at least one order."


def test_order_detail_display(driver):
    # Example test case for expanding order details might look like this.
    # You will need to adjust the selectors and logic based on the actual application.

    # Click the first order in the list to expand its details
    first_order = driver.find_element(By.CSS_SELECTOR, "#orderList > .orderRow:first-child")
    first_order.click()

    # Wait for the details to become visible
    details = WebDriverWait(driver, 5).until(
        EC.visibility_of(driver.find_element(By.ID, 'details'))
    )

    # Verify that the details contain expected information
    product_name = details.find_element(By.CSS_SELECTOR, ".productName").text
    assert product_name == "Product A", "Product name should match the one in the order details."

    quantity = details.find_element(By.CSS_SELECTOR, ".quantity").text
    assert int(quantity) == 10, "Quantity should match the one in the order details."

    price = details.find_element(By.CSS_SELECTOR, ".price").text
    assert float(price) == 2990.0, "Price should match the one in the order details."


if __name__ == '__main__':
    pytest.main()
