<H1> Application to verify the validity of the Vaccination Certificate
and extract data
</H1>

<H2> Authentication </H2>
The QR code is extracted from the PDF document, then the data from URL specified
in the QR code is compared with the personal data stated in the PDF certificate.

<H2> Data Extraction </H2>
The data obtained from the PDF of the vaccination certificate is written
to a file with cp1251 encoding. <br><br>
The data is written in the following form, one value per line: <br>
Last name <br>
Name <br>
Patronymic <br>
Date of birth <br>
Gender <br>
Identity document <br>
Date of introduction of the last vaccine <br>
The drug <br>

<h2> Running the program </h2>

pip install -r requirements.txt <br>
python main.py covid_certificate_path output_file_path

<h2> Running the program in Docker </h2>

The following commands should be executed: <br>
docker build --tag covid-parser . <br>
docker run -e v1='covid_certificate_path' -e v2='output_file_path' covid-parser
