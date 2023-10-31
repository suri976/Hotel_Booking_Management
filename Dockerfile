FROM python:3.8

WORKDIR /
# COPY requirements.txt .
COPY . .
RUN pip install -r requirements.txt

EXPOSE 8005
CMD ["python", "Hotel.py"]