import os
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selene.support.shared import browser
from dotenv import load_dotenv
from utils import attach

# Загружаем переменные окружения
load_dotenv()

SELENOID_URL = os.getenv("SELENOID_URL")
SELENOID_LOGIN = os.getenv("SELENOID_LOGIN", "")
SELENOID_PASS = os.getenv("SELENOID_PASS", "")
SELENOID_VIDEO_URL = os.getenv("SELENOID_VIDEO_URL", "")

# Настройки браузера
browser.config.base_url = "https://demoqa.com"
browser.config.window_width = 1920
browser.config.window_height = 1080

# Хук для скриншотов в случае падения теста
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.failed:
        screenshot_path = 'failure.png'
        browser.driver.save_screenshot(screenshot_path)  # <- исправлено
        allure.attach.file(
            screenshot_path,
            name='failure',
            attachment_type=allure.attachment_type.PNG
        )

# Фикстура для браузера
@pytest.fixture(scope="function", autouse=True)
def setup_browser():
    options = Options()
    options.set_capability("browserName", "chrome")
    options.set_capability("selenoid:options", {"enableVNC": True, "enableVideo": True})

    if SELENOID_URL:
        if SELENOID_LOGIN and SELENOID_PASS:
            remote_url = f"http://{SELENOID_LOGIN}:{SELENOID_PASS}@{SELENOID_URL}/wd/hub"
        else:
            remote_url = f"http://{SELENOID_URL}/wd/hub"

        driver = webdriver.Remote(
            command_executor=remote_url,
            options=options
        )
        browser.config.driver = driver

        yield browser

        # После теста добавляем артефакты
        attach.add_screenshot(browser)
        attach.add_logs(browser)
        attach.add_html(browser)
        attach.add_video(browser)

        driver.quit()
    else:
        # Локальный запуск
        driver = webdriver.Chrome(options=options)
        browser.config.driver = driver
        yield browser
        driver.quit()