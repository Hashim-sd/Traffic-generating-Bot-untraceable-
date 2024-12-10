# Required Libraries
import random
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import undetected_chromedriver as uc
from faker import Faker


# Constants
SCROLL_PAUSE_TIME = 0.5  # Time to wait after each scroll action (simulates human-like interaction)


def get_random_proxy():
    """
    Returns a random proxy from a predefined list.
    Ensures that proxies are used for anonymizing requests.
    """
#proxie ip and port could be added more than 3
    proxies = [
        "http://178.62.223.189:34103",
        "http://113.123.0.14:57114",
        "http://190.109.75.253:33633"
    ]
    return random.choice(proxies)


def test_proxy(proxy):
    """
    Tests if the provided proxy is functional by making an HTTP request to a known URL.
    If the proxy is working, it will return True, otherwise False.
    """
    try:
        response = requests.get("http://example.com", proxies={"http": proxy, "https": proxy}, timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def configure_browser(proxy=None):
    """
    Configures the Chrome browser for the traffic bot.
    Sets up proxies, random user-agent, and disables features that may cause detection.
    """
    options = uc.ChromeOptions()

    # Randomize user-agent to simulate various devices and browsers
    user_agent = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/{random.randint(530, 537)}.{random.randint(1, 36)} (KHTML, like Gecko) Chrome/{random.randint(90, 108)}.0.{random.randint(2000, 5000)} Safari/{random.randint(530, 537)}.{random.randint(1, 36)}"
    options.add_argument(f'user-agent={user_agent}')

    # Add proxy if provided, or skip if not available
    if proxy:
        options.add_argument(f'--proxy-server={proxy}')

    # Device Fingerprinting Spoofing (e.g., screen resolution, timezone)
    options.add_argument("--window-size=1920,1080")  # Fake screen resolution
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")  # Disables automation flags

    return uc.Chrome(options=options)


def simulate_mouse_movements(driver):
    """
    Simulates random human-like mouse movements to reduce the chances of detection.
    The bot moves the mouse cursor around the page in a random pattern.
    """
    action = ActionChains(driver)
    body = driver.find_element("tag name", "body")
    for _ in range(random.randint(5, 15)):
        x_offset = random.randint(-50, 50)
        y_offset = random.randint(-50, 50)
        action.move_to_element_with_offset(body, x_offset, y_offset).perform()
        time.sleep(random.uniform(0.1, 0.5))


def simulate_scrolling(driver):
    """
    Simulates human-like scrolling behavior by scrolling by random amounts.
    Random scrolls help in making the bot behavior less detectable.
    """
    for _ in range(random.randint(3, 7)):
        scroll_distance = random.randint(200, 1000)
        driver.execute_script(f"window.scrollBy(0, {scroll_distance});")
        time.sleep(random.uniform(1, 3))  # Pause between scrolls to mimic human behavior


def simulate_typing(driver, element, text):
    """
    Simulates human-like typing behavior by typing characters with random delays.
    This imitates the natural variation in typing speed and delays.
    """
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.1, 0.3))  # Delay between keystrokes to mimic human typing


def simulate_browsing(driver, url):
    """
    Simulates a user visiting a website, browsing it, scrolling, and typing.
    Adds human-like interactions including mouse movements and random delays.
    """
    driver.get(url)
    print(f"Visiting: {url}")

    # Simulate mouse movements
    simulate_mouse_movements(driver)

    # Simulate scrolling
    simulate_scrolling(driver)

    # Simulate human presence with delays between actions
    time.sleep(random.uniform(5, 10))


def main():
    """
    Main function that initializes and starts multiple sessions of browsing a specified URL.
    If proxies are available, it will use them, else it will proceed with a direct connection.
    """
    target_url = input("Enter the URL of the website you want the bot to target: ").strip()

    if not target_url.startswith("http://") and not target_url.startswith("https://"):
        print("Invalid URL! Please make sure the URL starts with 'http://' or 'https://'.")
        return

    # Session handling
    for session in range(3):  # Number of sessions to run
        print(f"Starting session {session + 1}")

        proxy = None
        driver = None
        try:
            # Check for working proxy
            for _ in range(3):  # Attempt to use up to 3 different proxies
                proxy = get_random_proxy()
                if test_proxy(proxy):
                    print(f"Using proxy: {proxy}")
                    break
            else:
                print("No valid proxy found. Proceeding without proxy.")
                proxy = None

            # Configure browser with proxy or direct connection
            driver = configure_browser(proxy=proxy)
            simulate_browsing(driver, target_url)

        except Exception as e:
            print(f"Error during session {session + 1}: {e}")

        finally:
            if driver:
                try:
                    driver.quit()  # Close the browser after session ends
                except Exception as cleanup_error:
                    print(f"Error during driver cleanup: {cleanup_error}")
                finally:
                    del driver  # Ensure proper cleanup to avoid memory leaks
            print(f"Session {session + 1} complete.\n")


if __name__ == "__main__":
    main()
