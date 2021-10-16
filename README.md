<H1> Приложение для проверки действительности Сертификата вакцинации 
и извлечения данных
</H1> 

<H2> Проверка подлинности </H2>
QR код извлекается из указанного документа PDF, затем полученные данные с URL, указанном 
в QR-коде, сравниваются с персональными данными, указанными в PDF сертификате.

<H2> Извлечение данных </H2>
Данные, получение из PDF сертификата вакцинации, записываются
в указанный файл в cp1251 кодировке. <br><br>
Данные записываются в следующем виде, одно значение на строку: <br>
Фамилия <br>
Имя <br>
Отчество <br>
Дата рождения <br>
Пол <br>
Документ удостоверяющий личность <br>
Дата введения последней вакцины <br>
Препарат <br>

<h2> Запуск программы </h2>

pip install -r requirements.txt
python main.py covid_certifivate_path output_file_path

<h2> Запуск программы в Docker </h2>

Необходимо выполнить следующие комманды: <br>
docker build --tag covid-parser . <br>
docker run -e v1='covid_certifivate_path' -e v2='output_file_path' covid-parser