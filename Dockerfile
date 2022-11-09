FROM python

ENV PYTHONUNBUFFERED 1

ADD requirements.txt .

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN pip install --upgrade setuptools 

RUN pip install -r requirements.txt

# agregar el directorio de la aplicación menos la carpeta de db_data
ADD . /my_app_dir/. 

WORKDIR /my_app_dir
