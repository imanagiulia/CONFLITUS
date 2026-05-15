from .conexao import get_db_connection

def inicializar_tabelas():
    """Cria a estrutura inicial do banco de dados."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS paises (
            nome TEXT PRIMARY KEY,
            latitude REAL,
            longitude REAL,
            em_conflito BOOLEAN DEFAULT 0
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fontes_dados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            instituicao TEXT,
            url_documento TEXT,
            data_coleta TEXT
        )
    ''')
    
    # Adicionar aqui a tabela de zonas_risco quando necessário
    conn.commit()
    conn.close()

def inserir_pais(nome, lat, lon):
    """Salva um país vindo da API no banco."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO paises VALUES (?, ?, ?, ?)', (nome, lat, lon, 0))
    conn.commit()
    conn.close()

def buscar_fontes():
    """Recupera todas as fontes registradas."""
    conn = get_db_connection()
    cursor = conn.cursor()
    fontes = cursor.execute('SELECT * FROM fontes_dados').fetchall()
    conn.close()
    return fontes

def registrar_fonte(instituicao, url, data):
    """Salva uma nova fonte de dados."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO fontes_dados (instituicao, url_documento, data_coleta) VALUES (?, ?, ?)', 
                   (instituicao, url, data))
    conn.commit()
    conn.close()


def buscar_coordenadas_pais(nome_pais):
    """Procura no banco a latitude e longitude de um país pelo nome."""
    conn = get_db_connection()
    cursor = conn.cursor()
    resultado = cursor.execute(
        'SELECT latitude, longitude FROM paises WHERE nome LIKE ?', 
        (f"%{nome_pais}%",)
    ).fetchone()
    conn.close()
    return resultado 

def buscar_todas_zonas_ativas():
    """Recupera todas as zonas de conflito registradas no banco."""
    conn = get_db_connection()
    cursor = conn.cursor()
    zonas = cursor.execute('SELECT latitude, longitude, raio_km, nivel_risco FROM zonas_risco').fetchall()
    conn.close()
    return zonas

def inserir_zona_risco(pais, lat, lon, raio_km, nivel_risco, populacao_afetada):
    """Salva uma nova zona de conflito baseada nos dados da ACLED."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Criamos a tabela caso ela não tenha sido criada ainda
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS zonas_risco (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pais_nome TEXT,
            latitude REAL,
            longitude REAL,
            raio_km REAL,
            nivel_risco TEXT,
            populacao_afetada INTEGER
        )
    ''')
    
    cursor.execute('''
        INSERT INTO zonas_risco (pais_nome, latitude, longitude, raio_km, nivel_risco, populacao_afetada)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (pais, lat, lon, raio_km, nivel_risco, populacao_afetada))
    
    conn.commit()
    conn.close()