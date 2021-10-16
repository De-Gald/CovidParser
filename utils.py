from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import cv2
import os
from subprocess import Popen, PIPE
import sys

# Аттрибуты
NUMBER = '№'
QR_CODE = 'QR-код сертификата'
PERSONAL_DATA = 'Персональные данные'
PERSONAL_DATA_ENG = 'Personal Data'
BIRTH_DATE = 'Дата рождения:'
SEX = 'Пол:'
DOCUMENT = 'Документ удостоверяющий личность'
ID = 'Серия и номер:'
FIRST_VACCINE = 'Первая вакцина'
SECOND_VACCINE = 'Вторая вакцина'
HOSPITAL = 'Медицинская организация'
DATE_OF_INJECTION = 'Дата введения вакцины:'
VACCINE = 'Препарат:'
MANUFACTURER = 'Производитель:'


def get_personal_data(text: str) -> (str, str, str, str, str, str):
    certificate_number = get_attribute_value(text, NUMBER, PERSONAL_DATA_ENG)
    fio = get_attribute_value(text, PERSONAL_DATA, BIRTH_DATE)
    last_name, first_name, middle_name = fio.split()
    date_of_birth = get_attribute_value(text, BIRTH_DATE, SEX)
    sex = get_attribute_value(text, SEX, DOCUMENT)
    doc_id = get_attribute_value(text, DOCUMENT, ID)

    return certificate_number, last_name, first_name, middle_name, date_of_birth, sex, doc_id


def get_vaccine_data(text: str) -> (str, str):
    injection_date = get_attribute_value(
        text,
        DATE_OF_INJECTION,
        VACCINE,
        flag=text.rfind(SECOND_VACCINE)
    )
    vaccine = (
        get_attribute_value(
            text,
            VACCINE,
            MANUFACTURER,
            flag=text.rfind(SECOND_VACCINE)).split('   ')[0]
    )
    return injection_date, vaccine


# Почучение значения поля, заданного как атрибут
def get_attribute_value(
    text: str,
    attribute: str,
    next_attribute: str,
    flag=0
) -> Optional[str]:
    attribute_start = text.rfind(attribute)

    if attribute_start > flag:
        attribute_end = attribute_start + len(attribute)
        next_attribute_start = text.rfind(next_attribute)

        return text[attribute_end:next_attribute_start].replace('\n', '').strip()


def get_webdriver() -> webdriver:
    chrome_options = Options()

    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    return webdriver.Chrome(options=chrome_options)


# Получение данных сертификата c URL, записанного в QR коде
def get_data_from_url(
    driver: webdriver,
    url: str
) -> (str, str, str):
    driver.get(url)

    certificate_number_url = driver.find_element_by_class_name('unrz').text
    date_of_birth_url = driver.find_element_by_xpath(
        '/html/body/div/div[2]/div[5]/div[2]/div[2]'
    ).text
    date_of_birth_url = date_of_birth_url.replace('.', '-')
    fio_url = driver.find_element_by_xpath('/html/body/div/div[2]/div[5]/div[1]/div[2]').text

    return certificate_number_url, fio_url, date_of_birth_url


def write_to_file(output_file: str, data: str):
    f = open(output_file, 'wb')
    f.write(data.encode('cp1251'))
    f.close()


def get_text_from_certificate(input_file: str) -> str:
    stdout = Popen(f'pdf2txt.py {input_file} --output-dir qrs', shell=True, stdout=PIPE).stdout
    text = stdout.read().decode('utf-8')

    return text


def get_url_from_qr_code():
    img = cv2.imread('qrs/img2.jpg')
    if img is None:
        print('Указанный документ не содержит QR код')
        sys.exit()
    detector = cv2.QRCodeDetector()
    url = detector.detectAndDecode(img)[0]
    os.system('rm qrs/*')

    return url
