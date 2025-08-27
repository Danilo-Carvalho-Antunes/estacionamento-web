# Checklist — Etapa 1 (Levantamento e requisitos)

Status geral: Pronto para revisão do time
Data: 2025-08-27

## Artefatos criados
- [x] `docs/requirements.md`
- [x] `docs/domain.puml`
- [x] `docs/user-stories.md`
- [x] `docs/api-spec.yaml`
- [x] `docs/adr/0001-clean-architecture.md`

## Validações
- [x] Cobertura de regras: fração, hora (1–9h), diária (>9h), noturna (entrada após 18:00 ou antes 06:00), mensalista, evento, capacidade, horário de funcionamento, rateio contratante.
- [x] Precisão monetária definida (Decimal/DECIMAL(10,2)) e moeda BRL.
- [x] Datas/horas em ISO 8601, armazenadas em UTC.
- [x] Erros padronizados (400/404/409/422) especificados na API; fila de espera com 202 Accepted.
- [x] Rastreabilidade ao legado (classes e método `controleAcesso()`).
- [x] Brainstorm documentado em `requirements.md`.

## Decisões A1–A5 (resolvidas)
- [x] A1: Arredondamento por frações de 15 min sempre para cima.
- [x] A2: Bordas 18:00/06:00 contam como noturna.
- [x] A3: Sobreposição de eventos determinada pelo horário de entrada.
- [x] A4: Capacidade com fila de espera (202 Accepted; status `queued`).
- [x] A5: `accrued_value` em BRL.
