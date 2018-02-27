FROM python:last
ADD ./image-gene.pyz /code/image-gene.pyz
ADD ./requirements/requirements.txt /code/requirements.txt
WORKDIR /code
RUN pip install -r requirements.txt
