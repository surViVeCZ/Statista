import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlencode

# Import existing functions
from scraper import setup_driver, login_with_selenium, log

# Define the base URL for Statista because, apparently, hardcoding is still cool sometimes
BASE_URL = "https://www.statista.com/studies-and-reports/all-reports"


def construct_url(topic=None):
    """
    Construct the dynamic URL based on the provided topic.
    If no topic is provided, return the default page URL.
    """
    params = {
        "idCountry": 0,
        "idBranch": 0,
        "idLanguage": 0,
        "reportType": 0,
        "documentTypes[]": "xls",
        "sortMethod": "idRelevance",
        "p": 1,
    }
    if topic:
        # Replace spaces with '+' because URLs are too cool for normal spaces
        params["q"] = topic.replace(" ", "+")
    return f"{BASE_URL}?{urlencode(params)}"


def extract_report_results(driver):
    """Extract and display report results with title, URL, and published date."""
    try:
        # Wait for those fancy report results to load
        results = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "reportResult"))
        )
        log.info("Report results located.")

        # Iterate through the results and extract the required details
        for result in results:
            # Extract the URL
            url = result.get_attribute("href")
            title = result.find_element(By.TAG_NAME, "h3").text.strip()

            # Extract the publication date
            published_in_element = result.find_element(
                By.XPATH,
                ".//span[contains(text(),'Published in')]/following-sibling::span",
            )
            published_in = (
                published_in_element.text.strip() if published_in_element else "N/A"
            )

            print(f"Title: {title}")
            print(f"URL: {url}")
            print(f"Published in: {published_in}")
            print("-" * 50)

    except Exception as e:
        log.error(f"An error occurred while extracting report results: {e}")


def open_xlsx_report_page(topic=None):
    """
    Navigate to the dynamically constructed XLSX report page and display results.
    :param topic: The topic to search for in the reports. Defaults to None.
    """
    driver = setup_driver()
    try:
        # Construct the URL
        page_url = construct_url(topic)
        log.info(f"Constructed URL: {page_url}")

        # Login to the website
        log.info("Starting login process...")
        if not login_with_selenium(driver):
            log.error("Login failed. Exiting script.")
            return

        # Navigate to the constructed URL
        log.info(f"Navigating to XLSX report page: {page_url}")
        driver.get(page_url)

        # Wait for the page to load completely
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        log.info("XLSX report page loaded successfully.")

        # Extract and display report results
        extract_report_results(driver)

    except Exception as e:
        log.error(f"An error occurred: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    log = logging.getLogger()

    # Prompt the user for a topic
    topic = input(
        "Enter a topic to search (or press Enter to load the default page): "
    ).strip()
    open_xlsx_report_page(topic if topic else None)
