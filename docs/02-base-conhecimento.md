# Base de Conhecimento

## Dados Utilizados

Descreva se usou os arquivos da pasta `data`, por exemplo:

| Arquivo | Formato | Qual a finalidade no AFIN? |
|---------|---------|---------------------|
| `historico_atendimento.csv` | CSV | Contextualizar interações anteriores e manter consistência nas respostas. |
| `perfil_investidor.json` | JSON | Simular perfis de usuários para personalizar explicações.|
| `produtos_financeiros.json` | JSON | Listar produtos financeiros genéricos para fins educativos. |
| `transacoes.csv` | CSV | 	Demonstrar padrões de gastos e organizar exemplos práticos de orçamento. |



---

## Adaptações nos Dados

Acrescentei mais produtos financeiros para que a resposta seja mais enriquecida. 

---

## Estratégia de Integração

### Como os dados são carregados?
Serão carregados via código, como no exemplo abaixo: 
```python
import pandas as pd
import json

# CSVs
historico = pd.read_csv('data/historico_atendimento.csv')
transacoes = pd.read_csv('data/transacoes.csv')

# JSONs
with open('data/perfil_investidor.json', 'r', endocoding='utf-8') as f:
    perfil = json.load(f)
with open('data/produtos_financeiros.json', 'r', endocoding ='utf-8') as f: 
    produtos = json.load(f)
```

### Como os dados são usados no prompt?

Para facilitar o entendimento, os dados podem ser injetados diretamente no prompt, oferecendo ao agente o melhor contexto possível para gerar respostas mais relevantes.

No entanto, em soluções mais robustas e escaláveis, o ideal é que essas informações sejam carregadas dinamicamente — permitindo maior flexibilidade, atualização contínua e adaptação ao perfil de cada usuário sem necessidade de modificar manualmente o prompt.

```text
{
  "nome": "João Silva",
  "idade": 32,
  "profissao": "Analista de Sistemas",
  "renda_mensal": 5000.00,
  "perfil_investidor": "moderado",
  "objetivo_principal": "Construir reserva de emergência",
  "patrimonio_total": 15000.00,
  "reserva_emergencia_atual": 10000.00,
  "aceita_risco": false,
  "metas": [
    {
      "meta": "Completar reserva de emergência",
      "valor_necessario": 15000.00,
      "prazo": "2026-06"
    },
    {
      "meta": "Entrada do apartamento",
      "valor_necessario": 50000.00,
      "prazo": "2027-12"
    }
  ]
}
```
```csv
data,descricao,categoria,valor,tipo
2025-10-01,Salário,receita,5000.00,entrada
2025-10-02,Aluguel,moradia,1200.00,saida
2025-10-03,Supermercado,alimentacao,450.00,saida
2025-10-05,Netflix,lazer,55.90,saida
2025-10-07,Farmacia,saude,89.00,saida
2025-10-10,Restaurante,alimentacao,120.00,saida
2025-10-12,Uber,transporte,45.00,saida
2025-10-15,Conta de Luz,moradia,180.00,saida
2025-10-20,Academia,saude,99.00,saida
2025-10-25,Combustí­vel,transporte,250.00,saida
```

---

## Exemplo de Contexto Montado

O exemplo abaixo foi construído a partir dos dados originais da base de conhecimento, mas sintetizado para destacar apenas as informações mais relevantes. Essa abordagem ajuda a otimizar o consumo de tokens e torna o prompt mais direto.

No entanto, é importante ressaltar que, em cenários práticos, a prioridade deve ser garantir que todas as informações essenciais estejam disponíveis para o agente. A economia de tokens é útil, mas nunca deve comprometer a qualidade ou a completude do contexto fornecido.

```text
Dados do Cliente:
- Nome: João Silva
- Idade: 32 anos
- Profissão: Analista de Sistemas
- Perfil: Moderado
- Renda mensal: R$ 5.000,00
- Patrimônio total: R$ 15.000,00
- Reserva de emergência atual: R$ 10.000,00
- Objetivo principal: Construir reserva de emergência

Metas:
- Completar reserva de emergência: R$ 15.000 até 06/2026
- Entrada do apartamento: R$ 50.000 até 12/2027

Total de Gastos:
- Moradia: R$ 1.380,00 (Aluguel R$ 1.200,00 + Conta de Luz R$ 180,00)
- Alimentação: R$ 570,00 (Supermercado R$ 450,00 + Restaurante R$ 120,00)
- Lazer: R$ 55,90 (Netflix R$ 55,90)
- Saúde: R$ 188,00 (Farmácia R$ 89,00 + Academia R$ 99,00)
- Transporte: R$ 295,00 (Uber R$ 45,00 + Combustível R$ 250,00)

Produtos disponíveis para explicar:
- Tesouro Selic → Altamente viável para completar a reserva de emergência, pois tem liquidez diária e baixo risco.
- CDB Liquidez Diária → Também viável, com rendimento um pouco superior ao Tesouro Selic, mas exige aporte mínimo maior.
- LCI/LCA → Pode ser considerado futuramente, mas não é ideal para reserva de emergência, já que exige prazo mínimo de 90 dias.
- Fundos Multimercado → Podem ser interessantes no futuro para diversificação, mas não são prioridade enquanto a reserva não estiver completa.
- Fundos de Ações → Não são viáveis neste momento, pois João declarou não aceitar risco e está focado em segurança

```

...
```
