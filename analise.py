#%%

from sqlalchemy import create_engine

DB_USER = "seu_usuario"
DB_PASSWORD = "sua_senha"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "seu_banco"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)