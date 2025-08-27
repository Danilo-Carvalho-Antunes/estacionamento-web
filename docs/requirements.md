# Requisitos — Estacionamento Web (Etapa 1)

## Escopo e objetivo
Migrar o sistema de estacionamento legado (CLI Java) para uma solução web com FastAPI + MySQL + React, preservando as regras de negócio e aprimorando separação de camadas (Clean Architecture).

## Atores e necessidades
- Gerente: administra estacionamentos, preços, eventos e associações.
- Operador/Usuário: realiza check-in/check-out, busca acessos.
- Cliente: consulta cotação.
- Contratante: acompanha receita acumulada.

## Regras de negócio (derivadas do legado)
1) Janela de funcionamento por estacionamento
   - Deve validar `opens_at` ≤ entrada < `closes_at`. Fora dessa janela, recusar check-in.
   - Fonte: `model/Estacionamento.getHoraAbertura()/getHoraFechamento()` e uso em `view/Main.controleAcesso()`.

2) Capacidade
   - Adotar fila de espera: quando ocupação atual ≥ capacidade, check-in retorna 202 (Accepted) com status `queued`.

3) Cálculo por tempo (Tipos tarifários)
   - Fração (< 1h): cobrança por blocos de 15 minutos, com arredondamento sempre para cima (ceiling).
   - 1–9h: valor por hora com desconto aplicado.
   - > 9h: diária. Se a entrada ocorrer às 18:00 ou depois, ou às 06:00 ou antes, aplicar diária noturna (percentual de desconto).
   - Fonte: `view/Main.controleAcesso()`, `model/Diaria`, `model/DiariaNoturna`.

4) Mensalista
   - Veículos associados ao estacionamento usam `monthly_value` (tarifa fixa) no check-out.

5) Eventos
   - Em janela de evento (data + horário do evento), prevalece `event.price` nas cotações/fechamento.
   - Evento aplicável é determinado pelo horário do acesso: usar o horário de entrada do acesso para identificar o evento vigente.

6) Rateio para contratante
   - Após cada cobrança, somar ao `accrued_value` o valor cobrado × `revenue_share_percent` do contratante. Valores em BRL (Real).

7) Cotação
   - Endpoint calcula valor e indica o tipo tarifário, sem registrar acesso.

## Políticas e validações
- Datas/horas: aceitar/retornar ISO 8601; armazenar UTC; frontend converte para fuso local.
- Precisão monetária: Decimal no backend; MySQL DECIMAL(10,2); moeda BRL.
- Erros: mensagens claras e consistentes (HTTP 400/404/409/422). Exemplos: fora do horário (409); capacidade usa fila de espera (202 Accepted, status `queued`); validação de payload (422); recurso inexistente (404).
- Logs: JSON estruturado no backend; incluir request_id e correlação básica.

## Casos-limite a validar
- Exatamente 60 minutos, 9 horas, fronteiras 18:00 e 06:00.
- Entrada fora do horário de funcionamento.
- Estacionamento lotado.
- Veículo mensalista associado vs. não associado.
- Evento ativo vs. inativo, sobreposição de eventos.

## Decisões de negócio (resolvidas)
- Frações de 15 minutos: arredondamento sempre para cima.
- Borda 18:00/06:00: conta como noturna.
- Eventos sobrepostos: determinado pelo horário de entrada do acesso (evento vigente na entrada).
- Capacidade: adotar fila de espera (202 Accepted; `status=queued`).
- `accrued_value`: moeda BRL (Real).

## Não-funcionais
- Testes automatizados para regras de preço (alvo >80% cobertura nos serviços e rotas críticas).
- Observabilidade básica (logs estruturados, saúde `/health`).
- Segurança (opcional nesta fase): JWT simples para Gerente/Operador; CORS.

## Brainstorm (mapa de requisitos)
- Quem: Gerente, Operador, Cliente, Contratante.
- O que: cadastrar lotes, preços, eventos, veículos; check-in/out; cotação; relatórios.
- Regras: janela de funcionamento, capacidade, tipos tarifários, mensalista, eventos, rateio.
- Exceções: fora do horário, lotado, dados inválidos, conflitos com eventos.
- Dados: lots, pricing_profiles, vehicles, associates, events, accesses, contractors.
- Relatórios: totals por contratante e por lote.

## Rastreabilidade ao legado
- `Projeto-OO-Intellij/src/view/Main.java` → `controleAcesso()` (lógica de cálculo e validações principais).
- `Projeto-OO-Intellij/src/model/Estacionamento.java` → horários e atributos do lote.
- `Projeto-OO-Intellij/src/model/Diaria.java` e `DiariaNoturna.java` → componentes de cálculo diário.

## Critérios de aceite da Etapa 1
- Este documento, `docs/domain.puml`, `docs/user-stories.md` e `docs/api-spec.yaml` concluídos e revisados.
- Regras de negócio totalmente cobertas e dúvidas registradas.
