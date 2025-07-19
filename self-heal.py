from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
import time
import logging

logging.basicConfig(level=logging.INFO)

# --- AI Agent to Heal Locators ---
class SelfHealingAgent:
    def __init__(self, driver):
        self.driver = driver

    def find_element(self, by, value):
        try:
            return self.driver.find_element(by, value)
        except NoSuchElementException:
            logging.warning(f"[AI Agent] Locator not found: {value}. Attempting to heal...")
            return self.heal_locator(value)

    def heal_locator(self, broken_value):
        page = self.driver.page_source
        soup = BeautifulSoup(page, 'html.parser')
        best_match = None
        best_score = 0

        for tag in soup.find_all():
            score = fuzz.partial_ratio(str(tag), broken_value)
            if score > best_score:
                best_score = score
                best_match = tag

        if best_match:
            logging.info(f"[AI Agent] Healed Locator Found with score {best_score}: {best_match.name}")
            try:
                healed_xpath = f"//{best_match.name}"
                return self.driver.find_element("xpath", healed_xpath)
            except:
                logging.error("[AI Agent] Healing failed. Element still not found.")
        else:
            logging.error("[AI Agent] No matching element found.")
        return None

# --- AI Failure Classifier ---
class FailureClassifier:
    def classify(self, exception):
        msg = str(exception)
        if "timeout" in msg.lower():
            return "Timeout Error"
        elif "no such element" in msg.lower():
            return "Element Not Found"
        elif "connection" in msg.lower():
            return "Network Issue"
        else:
            return "Unknown Error"

# --- Test Runner with AI Agent ---
def run_test():
    driver = webdriver.Chrome()
    agent = SelfHealingAgent(driver)
    classifier = FailureClassifier()

    try:
        driver.get("https://example.com")
        time.sleep(2)

        # Simulate broken locator
        element = agent.find_element("xpath", "//input[@id='nonexistent']")
        if element:
            element.send_keys("Testing Self-Healing Agent")

    except Exception as e:
        issue = classifier.classify(e)
        logging.error(f"[FailureClassifier] Exception: {e}")
        logging.error(f"[FailureClassifier] Classified as: {issue}")

    finally:
        driver.quit()

if __name__ == "__main__":
    run_test()
