import os
import time
import sys
import io
import glob
import shutil
import logging
from dotenv import load_dotenv
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# ChromeDriver auto-installer
import chromedriver_autoinstaller

# search for demonyms
from denonyms import get_demonym

# URL for advanced scraping option
xlsx_report_page = "https://www.statista.com/studies-and-reports/all-reports?idCountry=0&idBranch=0&idLanguage=0&reportType=0&documentTypes%5B%5D=xls&sortMethod=idRelevance&p=1"

# Constants and global variables
files_to_be_downloaded = 0  # Counter for files to download
failed_downloads = []  # List of failed download URLs
MAX_RETRIES = 2  # Retry limit for failed downloads
failed = 0

# Logging Configuration
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)  # Remove existing handlers

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),  # Console logging
        logging.FileHandler("scraper.log", mode="w", encoding="utf-8"),  # File logging
    ],
)
log = logging.getLogger()

# Load environment variables
load_dotenv()
USERNAME = os.getenv("STATISTA_USERNAME")
PASSWORD = os.getenv("STATISTA_PASSWORD")

# URLs and Configuration
LOGIN_URL = "https://www.statista.com/login/campus/"
TOPICS_URL = "https://www.statista.com/topics/"
DEST_FOLDER = os.path.abspath("statista_data")

# Ensure destination folder exists
os.makedirs(DEST_FOLDER, exist_ok=True)

# Ensure ChromeDriver is installed
chromedriver_autoinstaller.install()

# Initialize a session for HTTP requests
session = requests.Session()


def setup_driver():
    """Configure and return a Selenium WebDriver with headless mode."""
    options = Options()

    # Headless mode with additional compatibility arguments
    options.add_argument("--headless=new")  # New headless mode for Chrome
    options.add_argument("--disable-gpu")  # Disable GPU to avoid rendering issues
    options.add_argument("--window-size=1920,1080")  # Set window size for visibility
    options.add_argument("--force-device-scale-factor=1")  # Prevent scaling issues
    options.add_argument("--disable-dev-shm-usage")  # Prevent /dev/shm errors in Docker
    options.add_argument("--no-sandbox")  # Needed for running as root in some cases
    options.add_argument("--disable-extensions")  # Ensure extensions don't interfere
    options.add_argument("--disable-infobars")  # Suppress Chrome automation warnings
    options.add_argument(
        "--disable-blink-features=AutomationControlled"
    )  # Avoid detection

    # Experimental options for downloads
    options.add_experimental_option(
        "prefs",
        {
            "download.default_directory": DEST_FOLDER,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
        },
    )

    # Return configured WebDriver
    return webdriver.Chrome(options=options)


def login_with_selenium(driver):
    """Perform the login process using Selenium."""
    log.info("🔄 Starting Selenium login process...")
    driver.get(LOGIN_URL)

    # Step 1: Accept cookies
    try:
        accept_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Accept all')]")
            )
        )
        accept_button.click()
        log.info("✅ Cookies accepted successfully.")
    except Exception as e:
        log.warning(f"⚠️ Could not find 'Accept all' button: {e}")

    # Step 2: Select university and proceed
    try:
        university_dropdown = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "loginShibboleth_shibbolethLink"))
        )
        Select(university_dropdown).select_by_visible_text(
            "Brno University of Technology"
        )
        log.info("✅ Selected university: Brno University of Technology.")

        check_access_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "loginShibboleth_submitLoginCampus"))
        )
        check_access_button.click()
        log.info("✅ Clicked 'Check access' button.")
    except Exception as e:
        log.error(f"❌ Error during university selection: {e}")
        driver.quit()
        return False

    # Step 3: Enter username and password
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "frm-signInFormLogin-login"))
        )
        username_input = driver.find_element(By.ID, "frm-signInFormLogin-login")
        username_input.send_keys(USERNAME)
        log.info("✅ Username entered successfully.")

        submit_button = driver.find_element(By.NAME, "btnsubmit")
        submit_button.click()

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "frm-signInFormPassword-passwd"))
        )
        password_input = driver.find_element(By.ID, "frm-signInFormPassword-passwd")
        password_input.send_keys(PASSWORD)
        log.info("✅ Password entered successfully.")

        submit_button = driver.find_element(By.ID, "btnSubmit")
        submit_button.click()
        log.info("✅ Login form submitted.")
    except Exception as e:
        log.error(f"❌ Login form interaction failed: {e}")
        driver.quit()
        return False

    # Confirm successful login
    try:
        WebDriverWait(driver, 20).until(EC.url_contains("statista.com"))
        log.info(f"🎉 Login successful!")
        cookies = driver.get_cookies()
        for cookie in cookies:
            session.cookies.set(cookie["name"], cookie["value"])
        return True
    except Exception as e:
        log.error(f"❌ Login confirmation failed: {e}")
        driver.quit()
        return False


def search_topic(topic):
    """Search and return a list of URLs for topics that match
    the user's query (country name or its demonym)."""
    log.info(f'🔍 1/2 Searching for topics related to: "{topic}"...')

    # Get the demonym for the input topic
    demonym = get_demonym(topic)
    # Pre-lowercase them for easy matching
    topic_lower = topic.lower()
    demonym_lower = demonym.lower() if demonym else None

    page_number = 1
    matches = []

    while True:
        url = f"{TOPICS_URL}p/{page_number}/" if page_number > 1 else TOPICS_URL
        log.info(f"   Checking page: {url}")
        response = session.get(url)

        soup = BeautifulSoup(response.text, "html.parser")
        topic_boxes = soup.find_all("a", class_="panel-box")

        # Stop if no topics are found on this page
        if not topic_boxes:
            log.info("   ⚠️ Reached the end of pagination.")
            break

        for box in topic_boxes:
            href = box.get("href", "").strip()
            title_element = box.find("h2", class_="panel-box--title")
            topic_name = title_element.get_text(strip=True) if title_element else ""
            topic_name_lower = topic_name.lower()

            # Check if the user input OR its demonym is in the topic name
            if (topic_lower in topic_name_lower) or (
                demonym_lower and demonym_lower in topic_name_lower
            ):
                matches.append((topic_name, urljoin(TOPICS_URL, href)))

        page_number += 1

    if not matches:
        log.warning("⚠️ No topics found.")
        return []

    # Log and return matches
    # log.info("\nFound the following topics:")
    # for i, (name, _) in enumerate(matches, 1):
    #     log.info(f"[{i}] {name}")
    # log.info(f"[{len(matches) + 1}] Select all")
    return matches


def scrape_topic(topic_url):
    """Scrape data from the topic page, save chapters and sections, download report, and XLSX files."""
    global files_to_be_downloaded, failed_downloads

    log.info(f"🌐 Scraping topic page: {topic_url}")
    response = session.get(topic_url)
    if response.status_code != 200:
        log.error("❌ Failed to access topic page.")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    topic_name = topic_url.rstrip("/").split("/")[-1]
    topic_folder = os.path.join(DEST_FOLDER, topic_name)
    os.makedirs(topic_folder, exist_ok=True)
    raw_file = os.path.join(topic_folder, f"{topic_name}_sections_raw.txt")
    cleaned_file = os.path.join(topic_folder, f"{topic_name}_sections.txt")

    # If the cleaned file exists, use it; otherwise, create it
    if not os.path.exists(cleaned_file):
        log.info(f"🛠 Cleaned file not found. Creating a new one: {cleaned_file}")

        # Report section
        log.info("\n===== REPORT SECTION =====")
        explore_report_button = soup.find("a", class_="dossierTeaser__link")
        if explore_report_button:
            report_url = urljoin(
                "https://www.statista.com", explore_report_button["href"]
            )
            log.info(f"🔗 'Explore this report' URL found: {report_url}")
            download_report_with_selenium(report_url, topic_name)
        else:
            log.warning("⚠️ 'Explore this report' button not found on the topic page.")

        # Chapter & data scraping
        log.info("\n===== DATA SCRAPING SECTION =====")
        sources_section = soup.find("section", id="statisticChapter")
        if not sources_section:
            log.warning("⚠️ Sources section not found on the topic page.")
            return

        chapters = sources_section.find_all("div", class_="statisticChapter")
        section_urls = []
        logged_chapters = set()

        # Extract section URLs and log chapters
        with open(raw_file, "w", encoding="utf-8") as file:
            for chapter in chapters:
                chapter_title = (
                    chapter.find("h3").get_text(strip=True)
                    if chapter.find("h3")
                    else "Unknown Chapter"
                )
                if chapter_title not in logged_chapters:
                    file.write(f"Chapter: {chapter_title}\n")
                    log.info(f"📂 Chapter: {chapter_title}")
                    logged_chapters.add(chapter_title)

                for item in chapter.find_all("li", class_="statisticChapter__item"):
                    link = item.find("a")
                    if link:
                        section_name = link.text.strip()
                        section_url = urljoin("https://www.statista.com", link["href"])
                        file.write(f"  {section_name}: {section_url}\n")
                        section_urls.append(section_url)

        log.info(f"✅ Raw chapters and sections saved to {raw_file}")

        # Clean and reformat the raw file
        clean_and_reformat_file(raw_file, cleaned_file)
        os.remove(raw_file)
        log.info(f"✅ Cleaned chapters and sections saved to {cleaned_file}")
    else:
        log.info(f"✅ Using existing cleaned file: {cleaned_file}")

    # Read section URLs from the cleaned file, skipping lines starting with "Chapter:"
    log.info(f"🔄 Reading URLs from the cleaned file: {cleaned_file}")
    section_urls = []
    with open(cleaned_file, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line.startswith("Chapter:"):
                continue  # Skip lines starting with "Chapter:"
            if line and ":" in line:  # Identify section URL lines
                _, section_url = line.split(":", 1)
                section_urls.append(section_url.strip())

    # Update total files count early
    files_to_be_downloaded = len(section_urls)
    log.info(f"📊 Total files to be downloaded: {files_to_be_downloaded}")

    # Download all XLSX files
    log.info("🔄 Starting XLSX file download for all available section URLs...")
    with tqdm(
        total=files_to_be_downloaded, desc="Downloading XLSX files", unit="file"
    ) as pbar:
        for section_url in section_urls:
            download_xlsx(section_url, topic_folder, pbar)

        # Log failed downloads
    if failed_downloads:
        log.warning(f"⚠️ Failed downloads ({len(failed_downloads)}):")
        for failed_url in failed_downloads:
            log.warning(f"  - {failed_url}")


def download_xlsx(
    section_url, base_folder, pbar, subfolder="topic sections", retry_count=0
):
    """Download the XLSX file from the section URL and handle errors gracefully."""
    global failed_downloads, failed

    # Ensure the subfolder exists
    save_folder = os.path.join(base_folder, subfolder)
    os.makedirs(save_folder, exist_ok=True)

    driver = setup_driver()
    try:
        # Transfer cookies from the session to Selenium
        driver.get("https://www.statista.com/")  # Set domain for cookies
        for cookie in session.cookies:
            driver.add_cookie(
                {
                    "name": cookie.name,
                    "value": cookie.value,
                    "domain": cookie.domain,
                    "path": cookie.path,
                    "secure": cookie.secure or False,
                    "httpOnly": cookie.has_nonstandard_attr("httponly"),
                }
            )

        # Navigate to the section URL and initiate download
        # log.info(f"🔄 Navigating to section URL: {section_url}")
        driver.get(section_url)

        # Locate and click the XLS button
        try:
            xls_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//button[contains(@data-paywall-info-box-track, 'paywall_c2a--xls')]",
                    )
                )
            )
            xls_button.click()
            # log.info("📂 XLSX download initiated.")
            time.sleep(10)  # Wait for download to complete
        except Exception as e:
            log.error(f"❌ Failed to locate or click XLSX download button: {e}")
            raise

    except Exception as e:
        log.error(f"❌ Error during XLSX download from {section_url}: {e}")
        if retry_count < MAX_RETRIES:
            log.info(f"🔄 Retrying ({retry_count + 1}/{MAX_RETRIES})...")
            return download_xlsx(
                section_url, base_folder, pbar, subfolder, retry_count + 1
            )
        else:
            failed_downloads.append(section_url)
            failed += 1
            return
    finally:
        driver.quit()

    # Rename the downloaded file
    try:
        url_slug = section_url.rstrip("/").split("/")[-1]
        downloaded_files = glob.glob(os.path.join(DEST_FOLDER, "*.xls*"))
        if not downloaded_files:
            log.warning(f"⚠️ No downloaded file found for section: {url_slug}")
            return

        # Move the file to the appropriate folder
        downloaded_file = max(downloaded_files, key=os.path.getctime)
        save_path = os.path.join(save_folder, f"{url_slug}.xlsx")
        shutil.move(downloaded_file, save_path)
        log.info(f"📂 XLSX file saved: {os.path.basename(save_path)}")
        pbar.update(1)
    except Exception as e:
        log.error(f"❌ Failed to rename the downloaded file: {e}")


def get_failed_downloads():
    """Return the list of failed download URLs."""
    return failed


def download_report_with_selenium(report_url, topic_name):
    """Redirect to 'Explore this report' URL, open the Download dropdown, and click the PDF option."""
    driver = setup_driver()
    topic_folder = os.path.join(DEST_FOLDER, topic_name)
    os.makedirs(topic_folder, exist_ok=True)
    report_file_path = os.path.join(topic_folder, f"report_{topic_name}.pdf")

    try:
        # Transfer cookies from the session to the Selenium driver
        log.info("🔄 Transferring session cookies to Selenium browser...")
        driver.get(
            "https://www.statista.com/"
        )  # Open a page to set the domain for cookies
        for cookie in session.cookies:
            driver.add_cookie(
                {
                    "name": cookie.name,
                    "value": cookie.value,
                    "domain": cookie.domain,
                    "path": cookie.path,
                    "secure": cookie.secure or False,
                    "httpOnly": cookie.has_nonstandard_attr("httponly"),
                }
            )
        log.info("✅ Cookies transferred successfully.")

        # Ensure cookies are set
        time.sleep(5)  # Allow time for cookies to propagate
        driver.refresh()  # Refresh to apply cookies

        # Redirect to the report page
        log.info(f"🔄 Redirecting to report page: {report_url}")
        driver.get(report_url)

        # Hover over the Download button
        try:
            download_button = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID, "downloadButton"))
            )
            action = ActionChains(driver)
            action.move_to_element(download_button).perform()
        except Exception as e:
            log.error(f"❌ Failed to hover over the Download button: {e}")
            return

        # Wait for the dropdown to appear and click the PDF option
        try:
            pdf_option = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "dropdownButton__link--pdf"))
            )
            driver.execute_script("arguments[0].click();", pdf_option)
            log.info("🔄 PDF download initiated.")
            time.sleep(10)  # Wait for the download to complete
        except Exception as e:
            log.error(f"❌ Failed to locate or click the PDF download option: {e}")
            return
    finally:
        driver.quit()

    # Rename the downloaded file
    try:
        downloaded_files = glob.glob(os.path.join(DEST_FOLDER, "*.pdf"))
        if not downloaded_files:
            log.warning("⚠️ No downloaded file found.")
            return

        # Assume the most recently downloaded file is the target
        downloaded_file = max(downloaded_files, key=os.path.getctime)
        shutil.move(downloaded_file, report_file_path)
        log.info(f"📂 Report saved successfully at: {report_file_path}")
    except Exception as e:
        log.error(f"❌ Failed to rename the downloaded file: {e}")


def clean_and_reformat_file(input_file, output_file):
    """Clean and reformat the contents of the scraped file."""
    with (
        open(input_file, "r", encoding="utf-8") as infile,
        open(output_file, "w", encoding="utf-8") as outfile,
    ):
        current_chapter = None
        seen_sections = set()

        for line in infile:
            stripped_line = line.strip()

            if stripped_line.startswith("Chapter:"):
                current_chapter = stripped_line
                outfile.write(f"{current_chapter}\n")
                seen_sections.clear()
            elif stripped_line and ":" in stripped_line:
                section_name, section_url = stripped_line.split(":", 1)
                section_name = section_name.strip()
                section_url = section_url.strip()

                if (current_chapter, section_name) not in seen_sections:
                    outfile.write(f"  {section_name}: {section_url}\n")
                    seen_sections.add((current_chapter, section_name))


def get_files_to_be_downloaded(topic_url):
    log.info(f"Analyzing files to be downloaded for topic: {topic_url}")
    response = session.get(topic_url)
    if response.status_code != 200:
        log.error("❌ Failed to access topic page.")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    sources_section = soup.find("section", id="statisticChapter")
    if not sources_section:
        log.warning("⚠️ Sources section not found on the topic page.")
        return []

    section_urls = [
        urljoin("https://www.statista.com", link["href"])
        for chapter in sources_section.find_all("div", class_="statisticChapter")
        for item in chapter.find_all("li", class_="statisticChapter__item")
        if (link := item.find("a"))
    ]
    return len(section_urls) // 2


def main():
    """Main function to execute the scraper."""
    log.info("=" * 80)
    log.info("                       STATISTA SCRAPER - OPERATION LOG")
    log.info("=" * 80)

    driver = setup_driver()
    try:
        # LOGIN SECTION
        log.info("\n===== LOGIN SECTION =====")
        if login_with_selenium(driver):
            # TOPIC SEARCH SECTION
            log.info("\n===== TOPIC SEARCH SECTION =====")
            topic = input("Enter the topic to search (e.g., France): ").strip()
            selected_topics = search_topic(topic)

            if not selected_topics:
                log.warning("⚠️ No topics found for your search. Please try again.")
                return

            # Display topics and ask user to pick one or select all
            print("\nFound the following topics:")
            for i, (topic_name, _) in enumerate(selected_topics, 1):
                print(f"[{i}] {topic_name}")
            print(f"[{len(selected_topics) + 1}] Select all")

            while True:
                try:
                    choice = (
                        input(
                            "Enter the number of the topic you want to scrape (or 'all' to select all): "
                        )
                        .strip()
                        .lower()
                    )
                    if choice == "all" or choice == str(len(selected_topics) + 1):
                        # Process all topics
                        for topic_name, topic_url in selected_topics:
                            log.info(f"\n===== SCRAPING TOPIC: {topic_name} =====")
                            scrape_topic(topic_url)
                        break
                    elif choice.isdigit() and 1 <= int(choice) <= len(selected_topics):
                        # Process the selected topic
                        topic_name, topic_url = selected_topics[int(choice) - 1]
                        log.info(f"\n===== SCRAPING TOPIC: {topic_name} =====")
                        scrape_topic(topic_url)
                        break
                    else:
                        print("Invalid choice. Please try again.")
                except Exception as e:
                    log.error(f"❌ Error while processing selection: {e}")
        else:
            log.error("❌ Login failed. Exiting.")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
