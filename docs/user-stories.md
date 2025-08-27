# Histórias de Usuário (Etapa 1)

1) Gerente — Criar estacionamento
- Como Gerente, quero criar um estacionamento com horários e capacidade.
- CA: POST /lots cria registro; valida horários; GET /lots/{id} retorna dados.
- Exemplo (POST /lots):
```json
{
  "contractor_id": 1,
  "name": "Estac Centro",
  "capacity": 120,
  "opens_at": "06:00:00",
  "closes_at": "22:00:00"
}
```

2) Gerente — Configurar perfil de preços
- CA: PUT /lots/{id}/pricing aceita fracionado, desconto hora, diária, noturna, mensalista; GET reflete valores.
- Exemplo (PUT):
```json
{
  "fraction_value": "2.50",
  "hourly_discount_percent": "0.20",
  "daily_value": "35.00",
  "nightly_discount_percent": "0.30",
  "monthly_value": "250.00"
}
```

3) Operador — Check-in de veículo
- CA: POST /lots/{id}/access/check-in cria acesso open; valida dentro de horário e capacidade; 202 (status `queued`) se lotado.
- Exemplo (POST):
```json
{ "plate": "ABC1D23", "start_at": "2025-08-27T10:30:00Z" }
```

4) Operador — Check-out e valor calculado
- CA: POST /lots/{id}/access/check-out encerra acesso, retorna charged_value conforme regras.
- Exemplo (POST):
```json
{ "plate": "ABC1D23", "end_at": "2025-08-27T12:10:00Z" }
```

5) Operador — Listar acessos por placa e data
- CA: GET /lots/{id}/access?plate=&date= retorna acessos filtrados.

6) Gerente — Cadastrar evento com preço fixo
- CA: POST /lots/{id}/events cria; durante o evento, cotações usam price do evento.

7) Gerente — Associar veículo como mensalista
- CA: POST /lots/{id}/associates/{vehicle_id}; check-out usa monthly_value quando associado.

8) Cliente — Simular valor do estacionamento
- CA: GET /lots/{id}/quote?start_at=&end_at= retorna valor previsto e tipo tarifário.

9) Contratante — Ver receita acumulada
- CA: GET /reports/contractors/{id}/totals retorna accrued_value e breakdown.

10) Gerente — Fila de espera quando atingir capacidade
- CA: Check-in retorna 202 (status `queued`) quando ocupação ≥ capacidade; acesso efetivo é criado quando houver vaga.

Notas gerais
- Cancelar check-in não utilizado: fora de escopo no MVP.
- Mensagens de erro claras: 400/404/409/422 conforme caso.
