# Desafio: Transfers API com Assinatura HMAC + Idempotência

Implemente uma API de **transferências** que atenda aos requisitos abaixo.

## Objetivo

1. **Endpoint** `POST /transfers` que cria uma transferência.
2. A requisição **deve ser assinada** via **HMAC-SHA256** (cabeçalho `X-Signature`) usando um segredo compartilhado.
3. A criação deve ser **idempotente** via cabeçalho `X-Idempotency-Key`:
   - Primeira chamada com uma `X-Idempotency-Key` inédita e **payload P**: **201 Created**, retorna os dados da transferência criada.
   - Repetição da chamada com **mesma** `X-Idempotency-Key` e **mesmo payload P**: **200 OK** e retorna **a mesma** transferência (mesmo `id`) **sem criar outra**.
   - Repetição da chamada com **mesma** `X-Idempotency-Key` porém **payload diferente**: **409 Conflict**.
4. **Validação de assinatura HMAC**:
   - Calcular `signature = base64( HMAC_SHA256(secret, raw_body) )`.
   - Comparar com o header `X-Signature`. Se ausente ou incorreta: **401 Unauthorized**.
   - O segredo vem de `SIGNING_SECRET` (variável de ambiente).
5. **Consultas**:
   - `GET /transfers/{id}` retorna os dados de uma transferência existente (404 se não existir).

## Modelo sugerido

Tabela `transfers` (SQLite):
- `id` (int, PK)
- `amount` (int, em centavos, obrigatório, `>= 0`)
- `currency` (str, ex: "BRL", obrigatório)
- `beneficiary_account` (str, obrigatório)
- `idempotency_key` (str, **único**)
- `body_hash` (str, sha256 do corpo bruto da requisição)
- `created_at` (datetime, UTC sem timezone)

## Regras/observações

- Use **Python + FastAPI + SQLAlchemy + SQLite**.
- Use sempre **UTC naive** no banco (ex.: `datetime.utcnow()`).
- Não aceite requisições sem `X-Idempotency-Key` (responder 400).
- Estruture o código separando schemas, db, models e services.
- Inclua **testes** que cubram:
  - criação (201),
  - repetição idempotente com mesmo payload (200, mesmo `id`),
  - conflito de payload (409),
  - assinatura inválida/ausente (401),
  - busca por id (200/404).

## O que entregar

- Código fonte.
- `requirements.txt`.
- Testes (`pytest`).
- Opcional: `README.md` curto com instruções de execução.

Boa sorte!