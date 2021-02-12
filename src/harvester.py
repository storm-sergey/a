import time
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


CONTENT_CLASS_NAME = "content_3Gzc6maC"
LINK_QUESTION_CLASS_NAME = "link_question_31Iopbs3"
LINK_CATEGORY_CLASS_NAME = "link_category_lxzziIMq"
questions = list()
last_q_href = None
counter = 1


def harvest():
    global last_q_href, questions

    with open("log.json", "w") as log_file:
        json.dump({"questions": list()}, log_file, indent=2)

    with webdriver.Firefox() as driver:
        wait = WebDriverWait(driver, 1000)
        driver.get("https://otvet.mail.ru/")
        while True:
            new_questions = driver.find_elements(By.CLASS_NAME, CONTENT_CLASS_NAME)
            if last_q_href is None:
                last_q_href = new_questions[0].find_element(By.CLASS_NAME, LINK_QUESTION_CLASS_NAME).get_property('href')
            else:
                found: bool = find_last_question(new_questions)
                while not found:
                    time.sleep(1)
                    driver.find_element(By.XPATH, '//span[contains(text(), "Показать еще")]').click()
                    new_questions = driver.find_elements(By.CLASS_NAME, CONTENT_CLASS_NAME)
                    found = find_last_question(new_questions)

            add_to_log(new_questions)
            time.sleep(60)
            driver.refresh()


def add_to_log(new_questions):
    global questions
    with open("log.json", "r") as log_file:
        log = json.load(log_file)
        questions = log["questions"]
        questions.extend(collect(new_questions))
    with open("log.json", "w") as log_file:
        json.dump({"questions": questions}, log_file, indent=2)


def collect(new_questions) -> list:
    global counter
    question_list = list()
    for q in reversed(new_questions):
        question = dict()
        question["id"] = str(counter)
        question["question"] = q.find_element(By.CLASS_NAME, LINK_QUESTION_CLASS_NAME).text
        question["question link"] = q.find_element(By.CLASS_NAME, LINK_QUESTION_CLASS_NAME).get_property('href')
        question["category"] = q.find_element(By.CLASS_NAME, LINK_CATEGORY_CLASS_NAME).text
        question["category link"] = q.find_element(By.CLASS_NAME, LINK_CATEGORY_CLASS_NAME).get_property('href')
        question["timestamp"] = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        question_list.append(question)
        counter += 1
    return question_list


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
    """a mock"""
    return None


if __name__ == "__main__":
    harvest()
