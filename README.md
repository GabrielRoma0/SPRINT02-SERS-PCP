#  ChargeGrid Intelligence
### EV Challenge 2026 — Sprint 2 | FIAP x GoodWe | Grupo GTLF

> Da recarga residencial à plataforma comercial inteligente.

---

##  Integrantes

| Nome | RM |
|---|---|
| Fernando | 571408 |
| Gabriel | RM 570589 |
| Leo | 569556 |
| Thor Ferreira Camargo | RM 569543 |
| Rafael | 569729 |
| David | 568938 |

---

##  Sobre o Projeto

O **ChargeGrid Intelligence** é uma prova de conceito funcional para um sistema de gestão inteligente de eletropostos comerciais, desenvolvida como solução para o EV Challenge 2026 em parceria com a **GoodWe**.

O problema central: um carregador residencial (linha HCA G2 da GoodWe) atende bem um usuário individual, mas ambientes comerciais — como shoppings, condomínios e empresas — exigem gerenciamento simultâneo de múltiplos usuários, controle de demanda elétrica, tarifação individual e comunicação com sistemas centrais.

A solução proposta transforma o eletroposto de um simples fornecedor de kWh em um **hub de inteligência energética**.

---

##  Arquitetura do Sistema

O ChargeGrid Intelligence é organizado em três camadas:

```
┌─────────────────────────────────────────────────────┐
│  CAMADA DIGITAL                                     │
│  Controle de demanda · IA · APIs de pagamento       │
│  Automação em Python                                │
├─────────────────────────────────────────────────────┤
│  CAMADA DE CONECTIVIDADE                            │
│  Transmissão de dados em tempo real                 │
│  OCPP (carregadores) · MODBUS (medidores)           │
├─────────────────────────────────────────────────────┤
│  CAMADA FÍSICA                                      │
│  EV Charger GoodWe HCA G2 · Medidores de energia   │
│  Controladores de sessão                            │
└─────────────────────────────────────────────────────┘
```

**Fluxo de dados:**

```
Usuário conecta o veículo
        ↓
Sessão registrada via OCPP
        ↓
Medidor MODBUS envia dados de potência
        ↓
Controle de demanda distribui a carga disponível
        ↓
Consumo calculado em kWh por usuário
        ↓
Tarifa dinâmica aplicada (normal ou pico)
        ↓
Relatório gerado + orientação por IA
```

---

##  Prova de Conceito — `main.py`

A simulação em Python demonstra os 4 módulos operacionais do sistema:

### Módulo 01 — Simulação de Sessões
Representa usuários iniciando recargas em diferentes pontos do eletroposto. Gera dados de início, fim, duração e potência solicitada para cada sessão.

### Módulo 02 — Cálculo de Consumo
Calcula o consumo em **kWh por usuário** com base na potência alocada e na duração da sessão. Aplica tarifação diferenciada por horário:
- **Tarifa normal:** R$ 0,85/kWh (fora do pico)
- **Tarifa pico:** R$ 1,40/kWh (18h–21h)

### Módulo 03 — Controle de Demanda
Distribui a potência disponível entre os carregadores ativos, garantindo que a soma total respeite o **limite de demanda contratado (40 kW)**. Quando há sobrecarga, aplica um fator de redução proporcional a todos os pontos ativos — evitando multas e interrupções.

### Módulo 04 — Relatório e Orientação por IA
Gera um relatório consolidado com consumo individual, receita do operador e ocupação. Inclui uma **recomendação de IA** com análise de tarifação dinâmica, indicando ao usuário o melhor horário para recarregar com menor custo.

---

##  Energias Renováveis e Sustentabilidade

O ChargeGrid Intelligence conecta-se diretamente aos princípios de sustentabilidade energética:

**Eficiência no uso da rede elétrica**
O controle de demanda evita desperdício ao impedir sobrecargas e distribuir a potência disponível de forma inteligente, reduzindo perdas na instalação.

**Incentivo ao consumo fora do pico**
A tarifação dinâmica (mais barata fora das 18h–21h) desincentiva o uso em horários de maior carga na rede, contribuindo para o equilíbrio da demanda elétrica urbana — um princípio fundamental da gestão de redes inteligentes (smart grids).

**Compatibilidade com geração distribuída**
A arquitetura do sistema é compatível com integração de painéis solares (como os inversores GoodWe), permitindo que o eletroposto utilize energia gerada localmente para recargas, reduzindo a dependência da rede e a emissão de carbono associada.

**Mobilidade elétrica como vetor de sustentabilidade**
Cada kWh gerenciado de forma eficiente pelo ChargeGrid representa uma redução direta na emissão de CO₂ comparado ao uso de combustíveis fósseis, apoiando a transição energética no setor de transporte.

---

##  Como Executar

**Pré-requisitos:** Python 3.8 ou superior. Nenhuma biblioteca externa necessária.

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/chargegrid-intelligence.git
cd chargegrid-intelligence

# Execute a simulação
python3 main.py
```

**Saída esperada:**
```
══════════════════════════════════════════════════════════
  CHARGEGRID INTELLIGENCE — Simulação do Eletroposto
  EV Challenge 2026 | FIAP x GoodWe | Grupo GTLF
══════════════════════════════════════════════════════════

──── MÓDULO 01 — Simulação de Sessões ──────────────────
  [1] Ana      → Ponto 1 |   7.4 kW | 17:05–18:15 (70 min)
  [2] Bruno    → Ponto 2 |  11.0 kW | 17:10–18:30 (80 min)
  ...

──── MÓDULO 03 — Controle de Demanda ───────────────────
  Demanda solicitada : 47.8 kW
  Limite contratado  : 40.0 kW
  ⚠  Sobrecarga detectada! Fator de redução: 83.68%
  ...

──── IA — Orientação ao Usuário ────────────────────────
  Prefira carregar antes das 18h ou após as 21h.
  Economia potencial: 39.3% ao evitar o pico.
```

---

##  Estrutura do Repositório

```
chargegrid-intelligence/
│
├── chargegrid_simulation.py   # Prova de conceito — 4 módulos
├── README.md                  # Este arquivo
└── assets/                    # Diagramas e materiais de apoio
    └── Diagrama.png        # Diagrama das três camadas
```

---

## 🔗 Links

- 📹 Vídeo de apresentação (YouTube não listado): *fazendo...*
- 📋 Quadro Kanban: *https://trello.com/invite/b/6a2d691b1cb2f6822c716127/ATTIb3c23d907b09c441a7064f8cd9909d509BBFBD58/kanban-gtlf*

---

## Evolução em relação à Sprint 1

| Aspecto | Sprint 1 | Sprint 2 |
|---|---|---|
| Proposta | Conceitual | Funcional |
| Código | Esboço | Simulação completa (4 módulos) |
| Controle de demanda | Descrito | Implementado com fator proporcional |
| Tarifação | Descrita | Calculada dinamicamente por horário |
| IA | Conceito | Lógica de orientação ao usuário ativa |
| Relatório | Não existia | Gerado automaticamente por sessão |

---

*ChargeGrid Intelligence — FIAP x GoodWe · EV Challenge 2026*
