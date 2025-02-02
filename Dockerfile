# Basis-Image
FROM python:3.11

# Arbeitsverzeichnis setzen
WORKDIR /home/safashamari/projects/coderr_app

# Abhängigkeiten kopieren & installieren
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Projektdateien kopieren
COPY . .

# Statische Dateien sammeln
RUN python manage.py collectstatic --noinput

# Port für Gunicorn freigeben
EXPOSE 8000

# Gunicorn starten
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "coderr_app.wsgi:application"]
