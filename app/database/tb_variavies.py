import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

class VariaveisManager:
    def __init__(self, dev=False):
        """
        Inicializa o VariaveisManager com o modo de desenvolvimento.

        Args:
            dev (bool): Se True, gera o JSON após a consulta. Default é False.
        """
        load_dotenv()  # Carregar variáveis de ambiente do arquivo .env
        self.dev = dev
        self.engine = create_engine(
            f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
            f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        )

    def get_variaveis(self):
        """
        Consulta os dados da tabela 'tb_variaveis' e retorna um DataFrame.

        Returns:
            pd.DataFrame: DataFrame com os dados da tabela 'tb_variaveis'.
        """
        query = "SELECT * FROM tb_variaveis"
        df = pd.read_sql(query, self.engine)
        
        if self.dev:
            self._save_as_json(df)
        
        return df

    def _save_as_json(self, df):
        """
        Salva o DataFrame em um arquivo JSON na pasta 'result'.

        Args:
            df (pd.DataFrame): DataFrame a ser salvo como JSON.
        """
        result_dir = "result"
        os.makedirs(result_dir, exist_ok=True)  # Cria a pasta se não existir
        
        file_path = os.path.join(result_dir, "tb_variaveis.json")
        df.to_json(file_path, orient="records", indent=4, force_ascii=False)
        print(f"JSON salvo em: {file_path}")

# Exemplo de uso
if __name__ == "__main__":
    # Inicializa o gerenciador em modo de desenvolvimento para gerar JSON
    manager = VariaveisManager(dev=True)
    df = manager.get_variaveis()
    print(df.head())  # Exibe os primeiros registros do DataFrame

