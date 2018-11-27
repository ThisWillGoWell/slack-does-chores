FROM python:3.7.1-stretch
COPY requirments.txt /app/
WORKDIR /app/
RUN pip install -r requirments.txt
COPY * /app/
EXPOSE 80
CMD ["python", "app.py"]

