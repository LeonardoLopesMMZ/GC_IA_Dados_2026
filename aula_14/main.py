from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import requests

FRUITYVICE_URL = "https://www.fruityvice.com/api/fruit"

app = FastAPI(title="API da Casa de Sucos")

sucos: dict[int, dict] = {}
proximo_id = 1


class SucoEntrada(BaseModel):
    nome: str
    frutas: list[str] = Field(min_length=1)
    tem_gosto_de: str


class SucoAtualizacao(BaseModel):
    frutas: list[str] = Field(min_length=1)


def buscar_fruta(nome: str) -> dict:
    try:
        resposta = requests.get(f"{FRUITYVICE_URL}/{nome.strip()}", timeout=10)
    except requests.RequestException:
        raise HTTPException(
            status_code=503,
            detail="Não foi possível consultar a API Fruityvice no momento. Tente novamente.",
        )
    if resposta.status_code == 404:
        raise HTTPException(
            status_code=404,
            detail=f"Fruta '{nome}' não encontrada. Verifique o nome (em inglês) e tente novamente.",
        )
    if resposta.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail="A API Fruityvice retornou um erro inesperado.",
        )
    return resposta.json()


def calcular_totais(frutas: list[str]) -> tuple[float, float]:
    total_calorias = 0.0
    total_acucar = 0.0
    for nome in frutas:
        nutricao = buscar_fruta(nome)["nutritions"]
        total_calorias += nutricao["calories"]
        total_acucar += nutricao["sugar"]
    return round(total_calorias, 2), round(total_acucar, 2)


@app.get("/frutas/{nome}")
def consultar_fruta(nome: str):
    fruta = buscar_fruta(nome)
    return {
        "nome": fruta["name"],
        "calorias": fruta["nutritions"]["calories"],
        "acucar": fruta["nutritions"]["sugar"],
    }


@app.post("/sucos", status_code=201)
def cadastrar_suco(suco: SucoEntrada):
    global proximo_id
    total_calorias, total_acucar = calcular_totais(suco.frutas)
    novo = {
        "id": proximo_id,
        "nome": suco.nome,
        "frutas": suco.frutas,
        "tem_gosto_de": suco.tem_gosto_de,
        "total_calorias": total_calorias,
        "total_acucar": total_acucar,
    }
    sucos[proximo_id] = novo
    proximo_id += 1
    return novo


@app.get("/sucos")
def listar_sucos():
    return list(sucos.values())


@app.put("/sucos/{id}")
def atualizar_suco(id: int, dados: SucoAtualizacao):
    if id not in sucos:
        raise HTTPException(status_code=404, detail=f"Suco com id {id} não encontrado.")
    total_calorias, total_acucar = calcular_totais(dados.frutas)
    sucos[id].update(
        frutas=dados.frutas,
        total_calorias=total_calorias,
        total_acucar=total_acucar,
    )
    return sucos[id]
