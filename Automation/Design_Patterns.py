# Page Object Model (POM) implementation in Python using Selenium PageFactory
from selenium.webdriver.common.by import By
from selenium.webdriver.support.page_factory import PageFactory, init_elements, locator
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from typing import Any
from datetime import timedelta

class PageGoogle(PageFactory):
    def __init__(self, driver: WebDriver):
        self.driver = driver
        init_elements(driver, self)

    # Locators
    search_field: WebElement = locator((By.NAME, "q"))
    search_result: WebElement = locator((By.PARTIAL_LINK_TEXT, "BlazeMeter Continuous Testing | BlazeMeter by Perforce"))

    # Actions
    def search_google(self, search_term: str):
        self.search_field.send_keys(search_term)
        self.search_field.submit()

    def is_search_result_found(self) -> bool:
        try:
            return WebDriverWait(self.driver, 5).until(
                EC.visibility_of(self.search_result)
            ) is not None
        except Exception:
            return False

# Usage 
from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://www.google.com")

page = PageGoogle(driver)
page.search_google("BlazeMeter Continuous Testing")

if page.is_search_result_found():
    print("✅ Search result found")
else:
    print("❌ Search result not found")

driver.quit()

# Singleton Pattern for WebDriver in Python
from selenium import webdriver

class WebDriverSingleton:
    _instance = None   # private class variable

    def __new__(cls):
        """Prevent direct instantiation (Singleton)."""
        raise RuntimeError("Use get_instance() instead")

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            # You can configure ChromeOptions/FirefoxOptions here if needed
            cls._instance = webdriver.Chrome()
        return cls._instance

    @classmethod
    def close_driver(cls):
        if cls._instance is not None:
            cls._instance.quit()
            cls._instance = None
# Usage
# Get the same driver instance anywhere
driver = WebDriverSingleton.get_instance()
driver.get("https://www.google.com")

# Get again → returns same instance
same_driver = WebDriverSingleton.get_instance()
print(driver == same_driver)  # True ✅

# Close when finished
WebDriverSingleton.close_driver()

# Factory Design Pattern for creating WebDriver instances in Python
# POM
from selenium import webdriver

class WebDriverFactory:
    @staticmethod
    def create_driver(browser_type: str):
        browser_type = browser_type.lower()

        if browser_type == "chrome":
            return webdriver.Chrome()
        elif browser_type == "firefox":
            return webdriver.Firefox()
        elif browser_type == "edge":
            return webdriver.Edge()
        else:
            raise ValueError(f"Unsupported browser type: {browser_type}")

# Usage
# Example: Create Chrome driver
driver = WebDriverFactory.create_driver("chrome")
driver.get("https://www.google.com")

# Example: Create Firefox driver
# driver = WebDriverFactory.create_driver("firefox")

driver.quit()

# Facade Design Pattern example in Python Selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


class HomePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.search_box = (By.NAME, "search_query")

    def search_item(self, item_name: str):
        self.driver.find_element(*self.search_box).send_keys(item_name)
        self.driver.find_element(*self.search_box).submit()


class SearchResultsPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.first_item = (By.CSS_SELECTOR, ".product-container a.product_img_link")

    def select_first_item(self):
        self.driver.find_element(*self.first_item).click()

# Facade Class (hides complexity)
class ProductPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.add_to_cart_btn = (By.NAME, "Submit")

    def add_to_cart(self):
        self.driver.find_element(*self.add_to_cart_btn).click()

class PlaceOrderFacade:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.home = HomePage(driver)
        self.results = SearchResultsPage(driver)
        self.product = ProductPage(driver)

    def place_order(self, item_name: str):
        try:
            self.home.search_item(item_name)
            self.results.select_first_item()
            self.product.add_to_cart()
            # checkout steps can be added here...
            return "Order placed successfully"
        except Exception as e:
            return f"Error: {str(e)}"

# Test (Facade hides POM details)
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


class TestFacadeDesign:
    def setup_method(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.get("http://automationpractice.com/index.php")
        self.driver.maximize_window()
        self.facade = PlaceOrderFacade(self.driver)

    def test_place_order(self):
        result = self.facade.place_order("dress")
        assert result == "Order placed successfully"

    def teardown_method(self):
        self.driver.quit()

# Key Benefits:

# POM Classes (HomePage, SearchResultsPage, ProductPage) handle their own locators/actions.

# Facade (PlaceOrderFacade) ties them together into one simple place_order() call.

# Test only knows about the facade, not the inner details → much cleaner & maintainable.
