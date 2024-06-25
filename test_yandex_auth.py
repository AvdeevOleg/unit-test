import time

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

from config import YANDEX_LOGIN, YANDEX_PASSWORD


@pytest.fixture
def browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Опция запуска браузера в фоновом режиме
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


def test_yandex_login(browser):
    browser.get("https://passport.yandex.ru/auth/")

    # Найдите и заполните поле логина
    login_field = browser.find_element(By.ID, "passp-field-login")
    login_field.send_keys(YANDEX_LOGIN)
    login_field.send_keys(Keys.RETURN)

    time.sleep(2)  # добавьте задержку для загрузки следующей страницы

    # Найдите и заполните поле пароля
    password_field = browser.find_element(By.ID, "passp-field-passwd")
    password_field.send_keys(YANDEX_PASSWORD)
    password_field.send_keys(Keys.RETURN)

    time.sleep(5)  # добавьте задержку для загрузки следующей страницы

    # Проверяем, что авторизация прошла успешно
    # Например, проверяем наличие кнопки выхода
    try:
        browser.find_element(By.XPATH, "//a[contains(@href, 'logout')]")
        login_successful = True
    except:
        login_successful = False

    assert login_successful, "Авторизация на Яндексе не удалась"
