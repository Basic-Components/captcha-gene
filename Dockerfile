FROM python:last
ADD ./captcha_gene.py /code/captcha_gene.py
ADD ./requirements/requirements.txt /code/requirements.txt
WORKDIR /code
RUN pip install -r requirements.txt
