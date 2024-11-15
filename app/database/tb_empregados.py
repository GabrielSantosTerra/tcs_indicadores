import os
import sys
from dateutil import parser
from sqlalchemy import create_engine
from sqlalchemy.sql import text
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.api.empregados_api import APIClient  # Importa a classe da API


class EmpregadosDB:
    def __init__(self):
        self.engine = self._connect_to_db()

    def _connect_to_db(self):
        from dotenv import load_dotenv
        load_dotenv()

        db_url = (
            f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
            f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        )
        return create_engine(db_url)

    def delete_all(self):
        """
        Deleta todos os registros da tabela `tb_empregado`.
        """
        try:
            with self.engine.begin() as connection:  # Usando begin para garantir commit automático
                connection.execute(text("DELETE FROM public.tb_empregado"))
                print("Todos os registros foram deletados com sucesso.")
        except Exception as e:
            print(f"Erro ao deletar os registros: {e}")

    def save_data(self, df: pd.DataFrame):
        """
        Persiste os dados do DataFrame no banco de dados.
        """
        df = df.rename(
            columns={
                "name": "nome",
                "pis": "pis",
                "registration_number": "matricula",
                "cpf": "cpf",
                "admission_date": "dt_admissao",
                "job_title": "cargo",
                "team": "equipe",
                "business_unit": "unidade",
            }
        )

        # Função para limpar o formato da data
        def clean_date(date_str):
            try:
                # Remove o dia da semana (ex.: "Seg, ")
                date_str = date_str.split(", ")[1] if ", " in date_str else date_str
                # Converte para o formato yyyy-mm-dd
                return pd.to_datetime(date_str, format="%d/%m/%Y").strftime('%Y-%m-%d')
            except Exception:
                return None

        # Aplica a função de limpeza nas datas
        df["dt_admissao"] = df["dt_admissao"].apply(lambda x: clean_date(x) if pd.notnull(x) else None)

        # Adiciona a coluna `ano_mes_admissao`
        df["ano_mes_admissao"] = pd.to_datetime(df["dt_admissao"], errors="coerce").dt.strftime('%Y-%m')
        # Substitui valores NaN por None
        df = df.where(pd.notnull(df), None)

        try:
            # Insere os dados no banco
            df.to_sql("tb_empregado", con=self.engine, if_exists="append", index=False)
            print("Dados inseridos com sucesso.")
        except Exception as e:
            print(f"Erro ao salvar os dados: {e}")


# Exemplo de uso
if __name__ == "__main__":
    # Instancia o cliente da API
    api_client = APIClient(dev=False)
    df_empregados = api_client.get_empregados()

    # Extrai os dados da estrutura JSON
    data = df_empregados["data"][0]  # Navega para a chave 'data'
    df = pd.DataFrame(data)

    # Instancia a classe do banco
    db_manager = EmpregadosDB()

    # Executa a exclusão e depois a inserção
    print("Iniciando a exclusão de registros...")
    db_manager.delete_all()
    print("Exclusão concluída. Iniciando a inserção de registros...")
    db_manager.save_data(df)
