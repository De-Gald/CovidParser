FROM joyzoursky/python-chromedriver

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD python main.py $v1 $v2