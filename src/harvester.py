import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

last_q_href = None


def find_all_question(_webdr):
    return _webdr.find_elements(By.XPATH, '//a[contains(@class, "link_question_")]')


def show_more_questions(_webdr):
    _webdr.find_element(By.XPATH, '//span[contains(text(), "Показать еще")]').click()


def find_last_question(qs):
    global last_q_href
    for i in range(len(qs)):
        if qs[i].get_property('href') == last_q_href:
            last_q_href = qs[0].get_property('href')
            qs[:] = qs[:i]
            return True
    return False


def delay(d=1):
    time.sleep(d)


with webdriver.Firefox() as driver:
    counter = 1
    wait = WebDriverWait(driver, 1000)
    driver.get("https://otvet.mail.ru/")

    while True:  # сделай ограничение по дате
        questions = find_all_question(driver)
        if last_q_href is None:
            last_q_href = questions[0].get_property('href')
        else:
            found: bool = find_last_question(questions)
            while not found:
                delay(1)
                show_more_questions(driver)
                questions = find_all_question(driver)
                found = find_last_question(questions)

        f = open("log.txt", "a")
        for q in reversed(questions):
            f.write(str(counter) + ": " + q.get_property('href') + "\n[\"" + q.text + "\"]\n\n")
            counter += 1

        f.close()
        delay()
        driver.refresh()
