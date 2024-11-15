import os
import json
import requests
import pandas as pd
from dotenv import load_dotenv

class APIClient:
    def __init__(self, dev=False):
        load_dotenv()
        self.base_url = os.getenv("URL_BASE").rstrip('/')
        self.access_token = os.getenv("ACCESS_TOKEN")
        self.dev = dev

        if not self.base_url or not self.access_token:
            raise ValueError("URL_BASE ou ACCESS_TOKEN não configurados no arquivo .env")

    def get_empregados(self):
        url = f"{self.base_url}/reports/employees"
        headers = {
            "access-token": self.access_token,
            "Content-Type": "application/json"
        }

        payload = json.dumps({
            "report": {
                "group_by": "",
                "row_filters": "has_time_cards",
                "columns": "business_unit,name,pis,registration_number,job_title,team,cpf,admission_date",
                "format": "json",
                "filter_by": "business_unit_id",
                "business_unit_id": 309878
            }
        })

        try:
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()

            data = response.json()
            # print("Dados retornados pela API:", data)  # Debug dos dados retornados

            # Extrair os dados da chave 'data'
            if "data" in data and isinstance(data["data"], list) and len(data["data"]) > 0:
                rows = data["data"][0]  # Extrai a lista interna
                if isinstance(rows, list):
                    df = pd.DataFrame(rows)  # Converte para DataFrame
                else:
                    raise ValueError("Estrutura inesperada em 'data'")
            else:
                raise ValueError("Chave 'data' ausente ou vazia no retorno da API.")

            if self.dev:
                self._save_as_json(data)

            return df
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Erro ao conectar à API: {e}")
        except Exception as e:
            raise ValueError(f"Erro ao processar os dados: {e}")

    def _save_as_json(self, data):
        result_dir = "result"
        os.makedirs(result_dir, exist_ok=True)

        file_path = os.path.join(result_dir, "empregados.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"JSON salvo em: {file_path}")


# Exemplo de uso
if __name__ == "__main__":
    client = APIClient(dev=True)
    df = client.get_empregados()
    print(df.head())  # Exibe os primeiros registros do DataFrame
