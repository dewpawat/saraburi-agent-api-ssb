FROM python:3.12-slim-bookworm

# 1. ตั้งค่า Environment เพื่อให้ Python รันได้ลื่นไหลใน Container
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 2. ติดตั้ง System Dependencies
# รวมทั้ง MySQL Client และ Microsoft ODBC Driver 17
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    gcc \
    curl \
    gnupg2 \
    unixodbc-dev \
    && curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg \
    && curl -fsSL https://packages.microsoft.com/config/debian/12/prod.list | tee /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 3. ติดตั้ง Python Packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy Source Code
COPY app ./app
COPY .env ./ 

# 5. เปิด Port ตามที่คุณดิวตั้งไว้ในโปรเจกต์ (18080 หรือ 8000)
EXPOSE 18080

# 6. รัน FastAPI ด้วย uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "18080"]