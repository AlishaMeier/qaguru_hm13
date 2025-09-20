import pytest
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selene.support.shared import browser
from utils import attach


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()
    global selenoid_login, selenoid_pass, selenoid_url, selenoid_video_url
    selenoid_login = os.getenv("SELENOID_LOGIN", "")
    selenoid_pass = os.getenv("SELENOID_PASS", "")
    selenoid_url = os.getenv("SELENOID_URL")
    selenoid_video_url = os.getenv("SELENOID_VIDEO_URL", "")

    print("SELENOID_URL =", selenoid_url)
    print("SELENOID_VIDEO_URL =", selenoid_video_url)
    print("SELENOID_LOGIN =", "set" if selenoid_login else "empty")
    print("SELENOID_PASS =", "set" if selenoid_pass else "empty")


@pytest.fixture(scope="function", autouse=True)
def setup_browser():
    options = Options()
    caps = {
        "browserName": "chrome",
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        }
    }
    options.capabilities.update(caps)


    if selenoid_login and selenoid_pass:
        remote_url = f"http://{selenoid_login}:{selenoid_pass}@{selenoid_url}/wd/hub"
    else:
        remote_url = f"http://{selenoid_url}/wd/hub"

    driver = webdriver.Remote(
        command_executor=remote_url,
        options=options
    )

    browser.config.driver = driver

    yield browser


    attach.add_screenshot(browser)
    attach.add_logs(browser)
    attach.add_html(browser)
    attach.add_video(browser)

    driver.quit()