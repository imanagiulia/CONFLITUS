# 🌍 CONFLITUS

# Backend (Simulador Educativo de Conflito)

## 📖 Sobre o Projeto
O Projeto CONFLITUS tem como objetivo investigar problemas reais a partir de situações notáveis e dados públicos relacionados a Relações Públicas e suas ciências.O objetivo primário do projeto é demonstrar de forma visual os impactos humanitários de eventuais crises, zonas de risco, e as cadeias de escalada. 

Este repositório contém a **API REST (Backend)**, desenvolvida para processar dados geográficos, consumir APIs governamentais/globais, e executar o motor matemático de rotas para garantir o tráfego seguro de civis ou suprimentos desviando de zonas de risco.O sistema atua sem impor vieses políticos ou ideológicos, focando puramente no caráter educativo.

## 🚀 Funcionalidades da API

* **Ingestão de Dados (Pipeline):** Extração automatizada de coordenadas globais via REST Countries/CountriesNow e eventos de conflito reais via API da ACLED.
* **Cálculo de Impacto Humanitário:** Algoritmo que calcula o raio de impacto baseado na intensidade/fatalidades do conflito.
* **Motor de Rotas Seguro:** Avalia trajetos entre países. Caso a rota original intercepte uma zona de risco ativa, o sistema calcula e retorna uma rota alternativa de desvio seguro.
* **Rastreabilidade e Transparência:** Endpoints dedicados a informar as fontes oficiais (ACLED, ReliefWeb, UCDP) e as datas de coleta, garantindo o rigor acadêmico.

## 🛠️ Tecnologias Utilizadas

A arquitetura segue o modelo MVC (Model-View-Controller) adaptado para APIs, utilizando:
* **Python 3**
* **FastAPI & Uvicorn:** Framework principal de alta performance para a construção e documentação das rotas.
* **SQLite:** Persistência de dados locais de forma ágil.
* **Requests & python-dotenv:** Para consumo de APIs externas e gerenciamento de chaves de segurança via OAuth 2.0.

## 📂 Estrutura de Diretórios

O projeto foi organizado visando a separação de responsabilidades:

```text
backend/
├── app/
│   ├── controllers/    # Endpoints da API (Rotas, Simulação, Fontes)
│   ├── database/             # Conexão e queries SQL (SQLite)
│   ├── models.py       # Classes de dados e validação (Pydantic)
│   ├── pipeline.py     # Script de ingestão de dados e regras de ETL
│   └── main.py         # Arquivo de inicialização do FastAPI
├── data/               # Diretório onde o banco conflitus.db é gerado
├── .env                # Variáveis de ambiente (Segurança)
├── .gitignore          # Regras de exclusão do Git
└── requirements.txt    # Dependências do projeto
```

## ⚙️ Como executar o projeto localmente
### 1. Clonar o Repositório
```bash
git clone [https://github.com/seu-usuario/conflitus.git](https://github.com/seu-usuario/conflitus.git)
cd conflitus/backend
```
### 2. Configurar o Ambiente Virtual
```bash
python -m venv venv

# Ativar Windows:
venv\Scripts\activate

# Ativar Mac/Linux:
source venv/bin/activate
```
### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```
### 4. Configurar as Variáveis de Ambiente
Crie um arquivo .env na raiz da pasta backend:
```code
ACLED_EMAIL=seu_email@dominio.com
ACLED_PASSWORD=sua_senha
```
### 5. Executar o Pipeline de Dados
Para popular o banco SQLite inicial com países e zonas de conflito:
```bash
python -m app.pipeline
```
### 6. Iniciar o Servidor
```bash
uvicorn app.main:app --reload
```
Acesse a documentação interativa em: http://127.0.0.1:8000/docs
