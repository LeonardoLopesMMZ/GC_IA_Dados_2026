# API da Casa de Sucos

API desenvolvida em Python com FastAPI para gerenciar os sucos de uma Casa de Sucos. A aplicação consome a API pública [Fruityvice](https://www.fruityvice.com/api/fruit/) para buscar as informações nutricionais das frutas e calcular os valores de cada suco.

## Funcionalidades

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/frutas/{nome}` | Consulta uma fruta na Fruityvice e retorna nome, calorias e açúcar |
| POST | `/sucos` | Cadastra um suco, calculando o total de calorias e açúcar |
| GET | `/sucos` | Lista todos os sucos cadastrados |
| PUT | `/sucos/{id}` | (Bônus) Atualiza as frutas de um suco e recalcula os valores |

Os cálculos consideram **100 g** de cada fruta. Os nomes das frutas devem ser informados em inglês (ex.: `banana`, `strawberry`, `apple`), conforme a Fruityvice.

## Tratamento de erros

- Fruta não encontrada: `404` com mensagem amigável.
- Suco não encontrado (PUT): `404`.
- Fruityvice indisponível: `503`.

## Como executar

```bash
# 1. Entrar na pasta
cd aula_14

# 2. Criar e ativar o ambiente virtual
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux/macOS

# 3. Instalar as dependências
pip install -r requirements.txt

# 4. Iniciar a API
uvicorn main:app --reload
```

A documentação interativa (Swagger) fica em http://127.0.0.1:8000/docs.

## Exemplos

**POST /sucos**

```json
{
  "nome": "Vitamina Tropical",
  "frutas": ["banana", "strawberry"],
  "tem_gosto_de": "Tamarindo"
}
```

Resposta (`201`):

```json
{
  "id": 1,
  "nome": "Vitamina Tropical",
  "frutas": ["banana", "strawberry"],
  "tem_gosto_de": "Tamarindo",
  "total_calorias": 125.0,
  "total_acucar": 22.6
}
```

**PUT /sucos/1**

```json
{
  "frutas": ["banana", "strawberry", "apple"]
}
```

## Testes

Os testes realizados nos endpoints estão registrados em [testes.md](testes.md).

## Observações

Os sucos ficam armazenados em memória, então os dados são perdidos quando a API é reiniciada.
