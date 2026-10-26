# Testes realizados

Testes feitos nos endpoints da API (disponíveis no Swagger em `/docs`), na ordem abaixo.

## 1. GET /frutas/{nome}

Fruta existente (`banana`) - **200**

```json
{
  "nome": "Banana",
  "calorias": 96,
  "acucar": 17.2
}
```

Fruta inexistente (`xyzabc`) - **404**

```json
{
  "detail": "Fruta 'xyzabc' não encontrada. Verifique o nome (em inglês) e tente novamente."
}
```

## 2. POST /sucos

Corpo:

```json
{
  "nome": "Vitamina Tropical",
  "frutas": ["banana", "strawberry"],
  "tem_gosto_de": "Tamarindo"
}
```

Resposta - **201**

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

Com fruta inexistente (`abacaxizinho`) - **404**

```json
{
  "detail": "Fruta 'abacaxizinho' não encontrada. Verifique o nome (em inglês) e tente novamente."
}
```

## 3. GET /sucos - **200**

```json
[
  {
    "id": 1,
    "nome": "Vitamina Tropical",
    "frutas": ["banana", "strawberry"],
    "tem_gosto_de": "Tamarindo",
    "total_calorias": 125.0,
    "total_acucar": 22.6
  }
]
```

## 4. PUT /sucos/{id} (bônus)

Corpo (`/sucos/1`):

```json
{
  "frutas": ["banana", "strawberry", "apple"]
}
```

Resposta - **200**

```json
{
  "id": 1,
  "nome": "Vitamina Tropical",
  "frutas": ["banana", "strawberry", "apple"],
  "tem_gosto_de": "Tamarindo",
  "total_calorias": 177.0,
  "total_acucar": 32.9
}
```

Suco inexistente (`/sucos/99`) - **404**

```json
{
  "detail": "Suco com id 99 não encontrado."
}
```
