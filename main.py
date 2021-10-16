import sys

from utils import (
    get_data_from_url,
    get_personal_data, get_vaccine_data, get_webdriver,
    get_url_from_qr_code,
    get_text_from_certificate,
    write_to_file,
)

try:
    input_file = sys.argv[1]
    output_file = sys.argv[2]
except IndexError:
    print('Укажите пути к входному и выходному файлам')
    sys.exit()

# Получить весь текст PDF документа
text = get_text_from_certificate(input_file)

# Извлечь URL из QR кода сертификата
url = get_url_from_qr_code()

# Инициалировать Chrome Webdriver
driver = get_webdriver()

# Извлечение данных с полученного URL
certificate_number_url, fio_url, date_of_birth_url = get_data_from_url(driver, url)
last_name_url, first_name_url, middle_name_url = fio_url.split()

# Закрыть сессию Chrome
driver.close()

# Получение персональных данных человека из сертификата
certificate_number, last_name, first_name, middle_name, date_of_birth, sex, doc_id = (
    get_personal_data(text)
)

# Проверка, действительно ли данный сертификат принадлежит указанному человеку
# и является ли сертификат действительным
if (
    certificate_number == certificate_number_url
    and date_of_birth == date_of_birth_url
    and last_name[0] == last_name_url[0]
    and first_name[0] == first_name_url[0]
    and middle_name[0] == middle_name_url[0]
):
    # Получение даты введения второй вакцинации и её название
    injection_date, vaccine = get_vaccine_data(text)

    output_str = (
        last_name + '\n' +
        first_name + '\n' +
        middle_name + '\n' +
        date_of_birth + '\n' +
        sex + '\n' +
        doc_id + '\n' +
        injection_date + '\n' +
        vaccine
    )

    # Запись необходимых данных в указанный файл в кодировке cp1251
    write_to_file(output_file, output_str)

    print('Сертификат успешно обработан')
else:
    print('Сертификат не действителен!!!')
