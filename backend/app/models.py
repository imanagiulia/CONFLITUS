from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class Coordenada(BaseModel):
    latitude: float
    longitude: float

class Pais(BaseModel):
    nome: str
    coordenadas: List[Coordenada]
    em_conflito: bool
    aliancas: List[str] # Lista de nomes de países
    
    def obter_nivel_ameaca(self) -> str:
        return "Alto" if self.em_conflito else "Baixo"

class ZonaDeImpacto(BaseModel):
    epicentro: Coordenada
    raio_km: float
    nivel_risco: str
    populacao_afetada: int

    def calcular_raio(self, intensidade_conflito: int):
        # Exemplo didático: raio cresce com a intensidade
        self.raio_km = intensidade_conflito * 15.5 

    def estimar_impacto_humanitario(self, densidade_populacional: int):
        # Área do círculo * densidade
        area = 3.1415 * (self.raio_km ** 2)
        self.populacao_afetada = int(area * densidade_populacional)

class RotaDeTransporte(BaseModel):
    origem: str
    destino: str
    tipo: str  
    distancia_km: float
    status_seguranca: Optional[str] = None
    trajeto: List[Coordenada] = []

class FonteDeDados(BaseModel):
    instituicao: str
    url_documento: str
    data_atualizacao: date