import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlencode

# Import existing functions
from scraper import setup_driver, login_with_selenium, log

# Define the base URL for Statista because, apparently, hardcoding is still cool sometimes
BASE_URL = "https://www.statista.com/studies-and-reports/all-reports"


def construct_url(topic=None, page=1):
    """
    Construct the dynamic URL based on the provided topic and page number.
    If no topic is provided, return the default page URL.
    """
    params = {
        "idCountry": 0,
        "idBranch": 0,
        "idLanguage": 0,
        "reportType": 0,
        "documentTypes[]": "xls",
        "sortMethod": "idRelevance",
        "p": page,  # page
    }
    if topic:
        params["q"] = topic.replace(" ", "+")
    return f"{BASE_URL}?{urlencode(params)}"


def extract_report_results(driver, topic=None):
    """Extract and display report results with title, URL, and published date."""
    try:
        total_results = 0
        page = 1

        while True:
            # Construct the URL for the current page
            page_url = construct_url(topic, page)
            log.info(f"Navigating to page {page}: {page_url}")
            driver.get(page_url)

            # Try to load the report results; exit if no results are found
            try:
                results = WebDriverWait(driver, 5).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "reportResult"))
                )
            except Exception:
                log.info(f"No results found on page {page}. Stopping pagination.")
                break

            if not results:
                log.info("No more results found.")
                break

            log.info(f"Found {len(results)} reports on page {page}.")
            total_results += len(results)

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

            page += 1

        return total_results

    except Exception as e:
        log.error(f"An error occurred while extracting report results: {e}")


def open_xlsx_report_page(topic=None):
    """
    Navigate to the dynamically constructed XLSX report page and display results.
    :param topic: The topic to search for in the reports. Defaults to None.
    """
    driver = setup_driver()
    try:
        log.info("Starting login process...")
        if not login_with_selenium(driver):
            log.error("Login failed. Exiting script.")
            return

        # Extract and display report results
        advanced_reports = extract_report_results(driver, topic)
        log.info(f"Total advanced reports found: {advanced_reports}")

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

    # Prompt the user for a topic (will be removed later, needs to be integrated into the gui)
    topic = input(
        "Enter a topic to search (or press Enter to load the default page): "
    ).strip()
    open_xlsx_report_page(topic if topic else None)
