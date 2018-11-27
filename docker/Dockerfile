FROM python:3.7.1-stretch
COPY requirments.txt /app/
WORKDIR /app/
RUN pip install -r requirments.txt
COPY app.py /app/
COPY /src /app/src
COPY config.json /app/
COPY /templates /app/template
CMD ["python", "app.py"]

