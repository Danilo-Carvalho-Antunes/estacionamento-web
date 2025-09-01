# Backlog Seed — Estacionamento Web

Baseado em `docs/user-stories.md` (US1–US10) e nos protótipos em `docs/prototipos/` (01–08). Este arquivo estrutura épicos e itens para o board, com critérios de aceite. Conteúdo final, pronto para planejamento.

## Épicos e Itens

### EP-US1 — Criar estacionamento (Gestão de Estacionamentos)
- História: Como Gerente, quero criar um estacionamento com horários e capacidade.
- Protótipo: 03 (lista) e 03 (form).
- Frontend
  - FE-US1-01 Lista de estacionamentos (CRUD básico, paginação, busca).
  - FE-US1-02 Formulário de criação/edição (nome, capacidade, abre/fecha).
  - FE-US1-03 Validações de horário e mensagens de erro.
- Backend
  - BE-US1-01 POST/GET/PUT /lots com validações de horário/capacidade.
- Critérios de aceite
  - Criar/editar/listar funciona com validação de horários; erros 400/422 claros.

### EP-US2 — Configurar perfil de preços (Perfis de Preço)
- História: Como Gerente, quero configurar o pricing do estacionamento.
- Protótipo: 04.
- Frontend
  - FE-US2-01 Tela de edição de perfil de preços (fração, hora c/ desconto, diária, noturna, mensal).
  - FE-US2-02 Máscaras/formatos BRL e percentuais, validações.
- Backend
  - BE-US2-01 PUT/GET /lots/{id}/pricing.
- Critérios de aceite
  - Valores persistem e são refletidos nas consultas subsequentes.

### EP-US3 — Check-in (Terminal do Operador)
- História: Como Operador, quero realizar check-in de veículo.
- Protótipo: 01.
- Frontend
  - FE-US3-01 Ação de check-in com feedback de sucesso/erro.
  - FE-US3-02 Estado de lotado com retorno 202 e `queued` visível.
- Backend
  - BE-US3-01 POST /lots/{id}/access/check-in com validação de horário/capacidade.
- Critérios de aceite
  - Sucesso cria acesso aberto; lotado retorna 202 queued com posição.

### EP-US4 — Check-out e valor calculado (Terminal do Operador)
- História: Como Operador, quero encerrar o acesso e ver o valor devido.
- Protótipo: 01.
- Frontend
  - FE-US4-01 Ação de check-out exibindo `charged_value` formatado em BRL.
- Backend
  - BE-US4-01 POST /lots/{id}/access/check-out com cálculo de regras.
- Critérios de aceite
  - Cálculo aplica: frações (15min arredondando para cima), bordas noturnas (18:00/06:00), precedência de evento pela ENTRADA, mensalista = R$ 0,00.

### EP-US5 — Listar acessos (Terminal do Operador)
- História: Como Operador, quero listar acessos por placa e data.
- Protótipo: 01.
- Frontend
  - FE-US5-01 Filtros de placa/data e tabela.
- Backend
  - BE-US5-01 GET /lots/{id}/access?plate=&date=
- Critérios de aceite
  - Filtragem correta; estados vazios e erros padronizados.

### EP-US6 — Cadastrar evento (Eventos)
- História: Como Gerente, quero cadastrar eventos com preço fixo.
- Protótipo: 05 (lista) e 05 (form).
- Frontend
  - FE-US6-01 Lista de eventos; indicadores de período/ativo.
  - FE-US6-02 Form de criação/edição; aviso de sobreposição.
- Backend
  - BE-US6-01 POST/GET/PUT /lots/{id}/events.
- Critérios de aceite
  - Evento ativo impacta cotações (precedência pela ENTRADA).

### EP-US7 — Associar mensalista (Mensalistas)
- História: Como Gerente, quero associar veículo como mensalista.
- Protótipo: 06 (lista) e 06 (associar).
- Frontend
  - FE-US7-01 Lista de mensalistas; estados de pausa/cancelamento.
  - FE-US7-02 Modal de associar/pausar/cancelar com feedback.
- Backend
  - BE-US7-01 POST /lots/{id}/associates/{vehicle_id}.
- Critérios de aceite
  - Veículo associado tem check-out R$ 0,00.

### EP-US8 — Simular valor (Cotação Pública)
- História: Como Cliente, quero simular o valor entre início e fim.
- Protótipo: 08.
- Frontend
  - FE-US8-01 Página pública com formulário (lot, placa opcional, início/fim) e resultado com breakdown.
  - FE-US8-02 Badges de evento/noturna/mensalista; validação fim > início.
- Backend
  - BE-US8-01 GET /lots/{id}/quote?start_at=&end_at=
- Critérios de aceite
  - Retorna total estimado e tipo tarifário; formatações em BRL.

### EP-US9 — Relatórios do Contratante
- História: Como Contratante, quero ver receita acumulada e uso por período.
- Protótipo: 07.
- Frontend
  - FE-US9-01 KPIs + gráfico empilhado + tabela, filtros (período, lots, agrupamento).
  - FE-US9-02 Detalhamento por estacionamento (drawer/modal).
- Backend
  - BE-US9-01 GET /reports/contractors/{id}/totals.
- Critérios de aceite
  - Valores em BRL, agrupamentos corretos, exportação CSV (mock no FE).

### EP-US10 — Fila de espera (Capacidade)
- História: Como Operador, quero gerenciar fila quando lotado.
- Protótipo: 01 (estados de fila).
- Frontend
  - FE-US10-01 Exibir status queued e posição; feedback quando a vaga liberar.
- Backend
  - BE-US10-01 Check-in retorna 202 com payload de fila; promoção para acesso efetivo quando houver vaga.
- Critérios de aceite
  - Estados de fila visíveis; transição correta para acesso ativo.

## Roteiro MVP
US1 → US2 → US3 → US4 → US5 → US6 → US7 → US8 → US9 → US10.

## Definition of Done (geral)
- Critérios de aceite atendidos; formatação BRL; acessibilidade básica (foco, contraste, labels);
- Erros e estados vazios cobertos; mocks sem chamadas reais no protótipo;
- Documentação mínima atualizada (README de protótipos e referências de US).
