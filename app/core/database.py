from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# สำหรับ MS SQL Server (Async) เราจะใช้ mssql+aioodbc
# ต้องทำการ format connection string สำหรับ ODBC
connection_string = (
    f"DRIVER={{{settings.DB_DRIVER}}};"
    f"SERVER={settings.DB_HOST},{settings.DB_PORT};"
    f"DATABASE={settings.DB_NAME};"
    f"UID={settings.DB_USER};"
    f"PWD={settings.DB_PASS};"
)
#f"TrustServerCertificate=yes;" # สำคัญสำหรับ ODBC Driver 18

# สร้าง DATABASE_URL สำหรับ aioodbc
DATABASE_URL = f"mssql+aioodbc:///?odbc_connect={connection_string}"

# สร้าง engine แบบ Async
engine = create_async_engine(
    DATABASE_URL, 
    echo=False,
    pool_pre_ping=True # ช่วยตรวจสอบ connection ก่อนใช้งาน ป้องกันปัญหาต่อไม่ติด
)

async_session_factory = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with async_session_factory() as session:
        yield session