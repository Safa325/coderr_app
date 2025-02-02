# syntax=docker/dockerfile:1 <-- Bei manchen Systemen muss diese Zeile weg

FROM python:3.11



WORKDIR /usr/src/app


# docker run --publish 8000:8000 -it \
#   --mount type=bind,source=/Users/safashamari/Desktop/Developer/Python/coderr,target=/app \
#   coderr_database bash

COPY requirements.txt ./

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt



COPY . . 

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]