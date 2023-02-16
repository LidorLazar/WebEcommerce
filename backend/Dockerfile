
FROM python:3.10

ENV PYTHONUNBUFFERED 1

RUN git clone https://github.com/LidorLazar/WebEcommerce.git

WORKDIR /WebEcommerce/backend

RUN pip install virtualenv

RUN virtualenv env

RUN . env/Scripts/activate

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install python-decouple

ENV DJANGO_SETTINGS_MODULE=project.settings

ENV SECRET_KEY "django-insecure-beemfmt8c47l9&0qpnu(o*c($x*4@*$81amgsg))6zm-9wf$t2"

RUN python manage.py makemigrations

RUN python manage.py migrate

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]