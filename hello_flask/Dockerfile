

# Stage 1: Build Stage
FROM python:3.8-slim AS build
WORKDIR /app  

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libmariadb-dev \
    pkg-config

    COPY . .
RUN pip install --no-cache-dir -r requirements.txt

#STAGE 2 : production stage
FROM python:3.8-slim 
wORKDIR /app
COPY --from=build /app /app 
expose 5002
CMD ["python", "app.py"]