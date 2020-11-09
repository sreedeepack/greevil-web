FROM python:3.8.6
EXPOSE 8000

WORKDIR /usr/src/greevil-web/
COPY . .

#COPY requirements.txt .
#COPY requirements ./requirements
RUN pip install --no-cache-dir -r requirements.txt
#COPY . .


#RUN ./manage.py collectstatic --noinput
