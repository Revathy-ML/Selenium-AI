# Selenium-AI
Selenium with AI
`SelfHealingWebDriver` Class:
`__init__(self, driver)`: Initializes the self-healing driver with a standard Selenium `WebDriver` instance. It also creates `self.locators_history`, a dictionary to store the last successfully used locator (By strategy and value) for a given element name.
`find_element(self, by, value, element_name="")`: This is the core self-healing method.
First Attempt: It first tries to find the element using the provided `by` and `value`. If successful, it stores this locator in `locators_history` using `element_name` as a key.
`NoSuchElementException` Handling: If the initial attempt fails:
Historical Locator Check: It checks if a `element_name` was provided and if there's a historical locator for that element. If yes, it attempts to find the element using the historical locator. This is useful when an element's locator changes, but a previously known good locator still works.
Simple XPATH Fallback (Demonstration): If the historical locator also fails (or isn't available), it includes a very basic fallback for `By.ID` locators. It tries to construct an XPath `//*[@id='{value}']` based on the original `value`
