FROM python:3.8-slim
WORKDIR /app
COPY . .
RUN pip install flask redis
EXPOSE 5002
CMD ["python", "-m", "flask", "run", "--host", "0.0.0.0", "--port", "5002"]