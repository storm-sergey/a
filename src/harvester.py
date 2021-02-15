import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


CONTENT_CLASS_NAME = "content_3Gzc6maC"
LINK_QUESTION_CLASS_NAME = "link_question_31Iopbs3"
LINK_CATEGORY_CLASS_NAME = "link_category_lxzziIMq"
last_q_href = None
counter = 1


def harvest():
    global last_q_href
    with webdriver.Firefox() as driver:
        wait = WebDriverWait(driver, 1000)
        driver.get("https://otvet.mail.ru/")
        while True:
            questions = driver.find_elements(By.CLASS_NAME, CONTENT_CLASS_NAME)
            if last_q_href is None:
                last_q_href = questions[0].find_element(By.CLASS_NAME, LINK_QUESTION_CLASS_NAME).get_property('href')
            else:
                found: bool = find_last_question(questions)
                while not found:
                    time.sleep(1)
                    driver.find_element(By.XPATH, '//span[contains(text(), "Показать еще")]').click()
                    questions = driver.find_elements(By.CLASS_NAME, CONTENT_CLASS_NAME)
                    found = find_last_question(questions)

            f = open("log.txt", "a")
            f.write(collect(questions))
            f.close()
            time.sleep(300)
            driver.refresh()


def collect(questions) -> str:
    global counter
    c = ""
    for q in reversed(questions):
        c += "id: " + str(counter) + "\n"
        # question
        c += "question: \"" + q.find_element(By.CLASS_NAME, LINK_QUESTION_CLASS_NAME).text + "\"\n"
        c += "question link: " + q.find_element(By.CLASS_NAME, LINK_QUESTION_CLASS_NAME).get_property('href') + "\n"
        # category
        c += "category: \"" + q.find_element(By.CLASS_NAME, LINK_CATEGORY_CLASS_NAME).text + "\"\n"
        c += "category link: " + q.find_element(By.CLASS_NAME, LINK_CATEGORY_CLASS_NAME).get_property('href') + "\n"
        # date
        c += "timestamp: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "\n"
        c += "\n"
        counter += 1
    return c


def find_last_question(qs):
    global last_q_href
    for i in range(len(qs)):
        if qs[i].find_element(By.CLASS_NAME, LINK_QUESTION_CLASS_NAME).get_property('href') == last_q_href:
            last_q_href = qs[0].find_element(By.CLASS_NAME, LINK_QUESTION_CLASS_NAME).get_property('href')
            qs[:] = qs[:i]
            return True
    return False


def find_all_question(d):
    """this function is saved for the class names checking in the future feature"""
    return d.find_elements(By.XPATH, '//a[contains(@class, "link_question_")]')


def check_class_names():
    """mock"""
    return None


if __name__ == "__main__":
    harvest()
