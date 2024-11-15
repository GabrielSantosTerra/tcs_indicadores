import os
from sqlalchemy import create_engine

os.environ["DB_HOST"] = "jmfolha.postgresql.dbaas.com.br"
os.environ["DB_PORT"] = "5432"
os.environ["DB_NAME"] = "jmfolha"
os.environ["DB_USER"] = "jmfolha"
os.environ["DB_PASSWORD"] = "Tsc10012000%40"

db_url = "postgresql+psycopg2://jmfolha:Tsc10012000%40@jmfolha.postgresql.dbaas.com.br:5432/jmfolha"
try:
    engine = create_engine(db_url)
    connection = engine.connect()
    print("Conexão bem-sucedida!")
except Exception as e:
    print(f"Erro ao conectar ao banco de dados: {e}")