FROM python:3.9-slim
WORKDIR /app

# Install the application dependencies
COPY . /app
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python","main.py"]