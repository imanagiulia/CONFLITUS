import requests
import os
from datetime import date
from app.database import operacoes
from dotenv import load_dotenv

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_env = os.path.join(diretorio_atual, "..", "..", ".env")

load_dotenv(dotenv_path=caminho_env)

class PipelineDeDados:
    def __init__(self):
        operacoes.inicializar_tabelas()
        self.url_paises = "https://restcountries.com/v3.1/all"

    def executar_carga_paises(self):
        print("Iniciando carga de dados geográficos...")

        url_primaria = "https://restcountries.com/v3.1/all?fields=name,latlng"
        cabecalhos = {"User-Agent": "Mozilla/5.0"}
        
        try:
            print("Tentando conectar à API Primária...")
            resposta = requests.get(url_primaria, headers=cabecalhos, timeout=10)
            resposta.raise_for_status() 
            
            paises = resposta.json()
            paises_inseridos = 0
            
            for p in paises:
                nome = p.get('name', {}).get('common')
                latlng = p.get('latlng', [])
                if nome and len(latlng) == 2:
                    operacoes.inserir_pais(nome, latlng[0], latlng[1])
                    paises_inseridos += 1
            
            print(f"Sucesso na API Primária! {paises_inseridos} países salvos no SQLite.")
            return 
            
        except Exception as e:
            print(f"A API Primária falhou (Erro: {e}).")
            print("Ativando failover: Redirecionando para a API Secundária...")

        url_secundaria = "https://countriesnow.space/api/v0.1/countries/positions"
        
        try:
            resposta = requests.get(url_secundaria, timeout=10)
            resposta.raise_for_status()

            dados_json = resposta.json()
            paises = dados_json.get('data', [])
            
            paises_inseridos = 0
            for p in paises:
                nome = p.get('name')
                lat = p.get('lat')
                lon = p.get('long') 
                
                if nome and lat is not None and lon is not None:
                    operacoes.inserir_pais(nome, float(lat), float(lon))
                    paises_inseridos += 1
                    
            print(f"Sucesso na API Secundária! {paises_inseridos} países salvos no SQLite.")
            
        except Exception as e:
            print(f"A API Secundária também falhou: {e}")

    def executar_carga_acled(self):
        """Busca dados reais de conflitos na API da ACLED e salva como zonas de risco."""
        print("\nIniciando carga de dados de conflitos (ACLED)...")
        
        email = os.getenv("ACLED_EMAIL")
        senha = os.getenv("ACLED_PASSWORD")
        
        if not email or not senha:
            print("-> Aviso: Credenciais vazias. Ativando modo Mock...")

        try:
            print("Autenticando e gerando Token de Acesso (POST)...")
            url_auth = "https://acleddata.com/oauth/token"

            payload_auth = {
                "username": email,
                "password": senha,
                "grant_type": "password",
                "client_id": "acled"
            }
            
            resposta_auth = requests.post(url_auth, data=payload_auth, timeout=10)
            resposta_auth.raise_for_status()

            token = resposta_auth.json().get("access_token")
            
            if not token:
                print("Erro: A ACLED não retornou o token.")
                return

            print("Token gerado com sucesso! Buscando os eventos de conflito...")
            url_dados = "https://acleddata.com/api/acled/read?limit=50&event_type=Battles"

            cabecalhos_seguros = {
                "Authorization": f"Bearer {token}",
                "Accept": "application/json"
            }
            
            resposta_dados = requests.get(url_dados, headers=cabecalhos_seguros, timeout=15)
            resposta_dados.raise_for_status()
            
            dados = resposta_dados.json().get('data', [])
            zonas_inseridas = 0
            
            for evento in dados:
                pais = evento.get('country')
                lat = float(evento.get('latitude', 0.0))
                lon = float(evento.get('longitude', 0.0))
                fatalidades = int(evento.get('fatalities', 0))

                raio_calculado = 50.0 + (fatalidades * 5.0)
                nivel = "Crítico" if fatalidades > 10 else "Alto"

                operacoes.inserir_zona_risco(pais, lat, lon, raio_calculado, nivel, populacao_afetada=0)
                zonas_inseridas += 1
                
            print(f"Sucesso! {zonas_inseridas} zonas de conflito reais foram cadastradas no SQLite.")
            
        except requests.exceptions.HTTPError as e:
            print(f"-> Falha de comunicação com a ACLED. Código de erro: {e.response.status_code}")
            if e.response.status_code == 401:
                print("-> (Erro 401: Verifique se o email e a senha no seu .env estão corretos)")
        except Exception as e:
            print(f"-> Erro inesperado: {e}")

    def _inserir_zonas_teste(self):
        """Função Fallback: Insere dados simulados caso não tenha a chave da ACLED."""
        print("-> Injetando zonas de risco simuladas no SQLite...")
        # Simulando uma zona de conflito para testes de rotas
        operacoes.inserir_zona_risco("Ucrânia", 49.0, 32.0, 200.0, "Crítico", 50000)
        operacoes.inserir_zona_risco("Síria", 34.8, 38.9, 150.0, "Alto", 20000)
        print("-> Zonas de risco de teste (Mock) inseridas com sucesso!")

# --- Execução do Pipeline ---
if __name__ == "__main__":
    p = PipelineDeDados()
    p.executar_carga_paises()
    p.executar_carga_acled()