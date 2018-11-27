FROM python:3.7.1-stretch
COPY requirments.txt /app/
WORKDIR /app/
RUN pip install -r requirments.txt
COPY * /app/
COPY /src /app/src
CMD ["python", "app.py"]

