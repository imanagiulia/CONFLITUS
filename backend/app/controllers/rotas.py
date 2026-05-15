from fastapi import APIRouter, HTTPException
from app.models import RotaDeTransporte, ZonaDeImpacto, Coordenada
from app.database import operacoes
import math

router = APIRouter()

# --- AUXILIARES MATEMÁTICOS ---

def calcular_distancia(coord1, coord2):
    """Distância Haversine simplificada em KM."""
    dist_lat = (coord1.latitude - coord2.latitude) * 111.0
    dist_lon = (coord1.longitude - coord2.longitude) * 111.0
    return math.sqrt(dist_lat**2 + dist_lon**2)

def gerar_pontos_teste(origem, destino, passos=15):
    """Gera pontos ao longo da linha reta para testar colisões com zonas de risco."""
    pontos = []
    for i in range(passos + 1):
        f = i / passos
        lat = origem.latitude + (destino.latitude - origem.latitude) * f
        lon = origem.longitude + (destino.longitude - origem.longitude) * f
        pontos.append(Coordenada(latitude=lat, longitude=lon))
    return pontos

# --- LÓGICA DE DESVIO ---

@router.post("/tracar-rota")
def tracar_rota(origem: str, destino: str, tipo: str):
    # 1. Busca coordenadas reais no SQLite
    dados_origem = operacoes.buscar_coordenadas_pais(origem)
    dados_destino = operacoes.buscar_coordenadas_pais(destino)

    if not dados_origem or not dados_destino:
        raise HTTPException(status_code=404, detail="País de origem ou destino não encontrado no banco.")

    coord_a = Coordenada(latitude=dados_origem['latitude'], longitude=dados_origem['longitude'])
    coord_b = Coordenada(latitude=dados_destino['latitude'], longitude=dados_destino['longitude'])

    # 2. Busca zonas de risco reais no SQLite
    zonas_db = operacoes.buscar_todas_zonas_ativas()
    
    # 3. Teste de colisão na rota direta
    pontos_rota = gerar_pontos_teste(coord_a, coord_b)
    zona_conflito = None
    
    for ponto in pontos_rota:
        for z in zonas_db:
            dist = calcular_distancia(ponto, Coordenada(latitude=z['latitude'], longitude=z['longitude']))
            if dist <= z['raio_km']:
                zona_conflito = z
                break
        if zona_conflito: break

    # 4. Cálculo do Trajeto Final
    status = "Segura"
    trajeto = [coord_a, coord_b]

    if zona_conflito:
        status = "Desvio Calculado (Original Arriscada)"
        # Lógica de Desvio: Cria-se rota alternativa contornando a zona ao Norte
        margem = zona_conflito['raio_km'] + 50 
        waypoint = Coordenada(
            latitude=zona_conflito['latitude'] + (margem / 111.0),
            longitude=zona_conflito['longitude']
        )
        trajeto = [coord_a, waypoint, coord_b]

    return {
        "status": status,
        "detalhes": {
            "origem": origem,
            "destino": destino,
            "tipo_transporte": tipo,
            "coordenadas_trajeto": trajeto
        }
    }