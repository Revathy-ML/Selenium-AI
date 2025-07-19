from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class SelfHealingWebDriver:
    def __init__(self, driver):
        self.driver = driver
        self.locators_history = {} # Stores successful locators for elements

    def find_element(self, by, value, element_name=""):
        try:
            element = self.driver.find_element(by, value)
            if element_name:
                self.locators_history[element_name] = (by, value)
            return element
        except NoSuchElementException:
            print(f"Original locator failed for '{element_name}': By='{by}', Value='{value}'")
            if element_name and element_name in self.locators_history:
                original_by, original_value = self.locators_history[element_name]
                if (by, value) != (original_by, original_value):
                    print(f"Attempting to self-heal using historical locator for '{element_name}': By='{original_by}', Value='{original_value}'")
                    try:
                        element = self.driver.find_element(original_by, original_value)
                        print(f"Self-healing successful for '{element_name}'.")
                        return element
                    except NoSuchElementException:
                        print(f"Historical locator also failed for '{element_name}'.")
            
            # Simple example of a more advanced healing strategy (e.g., trying common alternatives)
            if by == By.ID:
                print(f"Attempting to self-heal by trying XPATH for ID: //*[@id='{value}']")
                try:
                    element = self.driver.find_element(By.XPATH, f"//*[@id='{value}']")
                    print(f"Self-healing successful for '{element_name}' using XPATH.")
                    if element_name:
                        self.locators_history[element_name] = (By.XPATH, f"//*[@id='{value}']")
                    return element
                except NoSuchElementException:
                    pass

            raise NoSuchElementException(f"Could not find element '{element_name}' with original or self-healed locators.")

# Usage Example:
if __name__ == "__main__":
    # Setup WebDriver (e.g., Chrome)
    driver = webdriver.Chrome() # Make sure you have chromedriver in your PATH or specify the path

    # Wrap the driver with the SelfHealingWebDriver
    s_driver = SelfHealingWebDriver(driver)

    try:
        driver.get("https://www.example.com") # Replace with a test URL

        # Simulate initial successful element finding
        print("\n--- Initial successful finding ---")
        element1 = s_driver.find_element(By.ID, "some_id", "Example Element") 
        print(f"Found element 1: {element1.tag_name}")

        # Simulate a scenario where the ID of 'some_id' changes to 'new_id'
        # To demonstrate, let's assume the HTML was: <div id="some_id">...</div>
        # And now it's: <div id="new_id">...</div>
        # Since we can't dynamically change the example.com HTML, this part is conceptual
        # In a real scenario, you'd modify the DOM or load a different page.
        
        # For demonstration purposes, let's manually update the history as if the original failed
        # and then we try a new, failing locator to trigger self-healing to the 'original'
        print("\n--- Simulating self-healing attempt ---")
        
        # First, let's pretend a *different* locator initially worked and is in history
        # This is to show the fallback to a known good locator.
        # In a real scenario, 'Example Element' would already be in history from a previous successful run.
        s_driver.locators_history["Example Element"] = (By.NAME, "some_name_that_works_initially")

        try:
            # Now, try to find it with a *failing* locator, expecting it to self-heal
            # If 'some_id_that_does_not_exist' fails, it will try the historical 'some_name_that_works_initially'
            element2 = s_driver.find_element(By.ID, "some_id_that_does_not_exist", "Example Element")
            print(f"Found element 2 (after self-healing): {element2.tag_name}")
        except NoSuchElementException as e:
            print(f"Caught expected exception during self-healing demo: {e}")

        # Another scenario: attempting to find an element whose ID changes, and then trying XPATH
        print("\n--- Simulating XPATH self-healing ---")
        try:
            # Assume 'non_existent_id' would usually resolve to 'some_xpath_for_it'
            # Here, we directly trigger the XPATH fallback since the ID fails.
            element3 = s_driver.find_element(By.ID, "non_existent_id", "XPath Test Element")
            print(f"Found element 3 (after XPATH self-healing): {element3.tag_name}")
        except NoSuchElementException as e:
            print(f"Caught expected exception when XPATH self-healing wasn't enough: {e}")
            # To truly test the XPATH self-healing, you'd need an element on example.com 
            # where an ID lookup fails but an XPATH lookup (like `//h1`) works.
            # Let's try to find the `<h1>` tag using a non-existent ID first, then fallback to XPATH.
            print("\n--- Actual XPATH self-healing test on existing element ---")
            try:
                # This will fail by ID, then our simple self-healing will try the XPATH for the ID value.
                # Since 'main_heading' is not an ID, it will then try //*[@id='main_heading'], which also fails.
                # The simple example given in the class will try //*[@id='{value}']
                # A more robust self-healing would need to know the actual alternatives.
                # For demonstration, let's force a successful XPATH find after an ID fail.
                element_heading = s_driver.find_element(By.ID, "definitely_not_a_real_id_for_h1", "Main Page Heading")
                print(f"Found main heading: {element_heading.text}")
            except NoSuchElementException as e:
                print(f"Still failing, but showing the concept of trying alternatives. {e}")
                # To successfully show the XPATH self-healing with the provided code:
                # The find_element for By.ID would need to be passed a value that, if converted to an XPATH
                # like //*[@id='{value}'] would actually find something.
                # This is a limitation of a simple general-purpose self-healing.
                # For example, if you wanted to find the h1:
                try:
                    print("Trying to find H1 using a direct XPATH for demo of fallback logic:")
                    element_h1_direct_xpath = s_driver.find_element(By.XPATH, "//h1", "Direct H1")
                    print(f"Found H1 directly: {element_h1_direct_xpath.text}")
                except NoSuchElementException as e:
                    print(f"Could not find H1: {e}")


    finally:
        driver.quit()
