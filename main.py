"""
ChargeGrid Intelligence 
EV Challenge 2026 | FIAP x GoodWe | Grupo GTLF

Módulos:
  01 - Simulação de sessões de recarga
  02 - Cálculo de consumo individual (kWh)
  03 - Controle de demanda (distribuição de potência)
  04 - Relatório de uso e custo estimado

Contexto: simula a operação de um eletroposto comercial com 4 pontos
de recarga, limite de demanda contratado e tarifação dinâmica por
horário de pico.
"""

import random
import time
from datetime import datetime, timedelta

# ─────────────────────────────────────────────
# CONFIGURAÇÃO DO ELETROPOSTO
# ─────────────────────────────────────────────
LIMITE_DEMANDA_KW = 40.0          # potência máxima contratada (kW)
NUM_PONTOS = 4                    # número de carregadores disponíveis
TARIFA_NORMAL = 0.85              # R$/kWh fora do pico
TARIFA_PICO   = 1.40              # R$/kWh no horário de pico (18h–21h)
HORA_PICO_INICIO = 18
HORA_PICO_FIM    = 21

# Potências disponíveis por tipo de carregador (kW)
POTENCIAS_DISPONIVEIS = {
    "Ponto 1": 7.4,
    "Ponto 2": 11.0,
    "Ponto 3": 22.0,
    "Ponto 4": 7.4,
}

# ─────────────────────────────────────────────
# SEPARADOR VISUAL
# ─────────────────────────────────────────────
def separador(titulo=""):
    linha = "─" * 56
    if titulo:
        print(f"\n{'─'*4} {titulo} {'─'*(50 - len(titulo))}")
    else:
        print(linha)


# ─────────────────────────────────────────────
# MÓDULO 01 — SIMULAÇÃO DE SESSÕES
# ─────────────────────────────────────────────
def simular_sessoes(num_sessoes=4):
    """
    Gera sessões de recarga simuladas para cada ponto do eletroposto.
    Cada sessão contém: usuário, ponto, hora de início, duração e
    potência solicitada.
    """
    separador("MÓDULO 01 — Simulação de Sessões")

    usuarios = ["Ana", "Bruno", "Carlos", "Débora", "Eduardo", "Flávia"]
    sessoes = []

    hora_base = datetime.now().replace(hour=17, minute=0, second=0, microsecond=0)

    for i, (ponto, potencia_max) in enumerate(POTENCIAS_DISPONIVEIS.items()):
        if i >= num_sessoes:
            break

        usuario = random.choice(usuarios)
        usuarios.remove(usuario)

        # Duração aleatória entre 20 e 90 minutos
        duracao_min = random.randint(20, 90)
        inicio = hora_base + timedelta(minutes=random.randint(0, 30))
        fim = inicio + timedelta(minutes=duracao_min)

        sessao = {
            "id": i + 1,
            "usuario": usuario,
            "ponto": ponto,
            "potencia_solicitada_kw": potencia_max,
            "inicio": inicio,
            "fim": fim,
            "duracao_min": duracao_min,
            "status": "ativa",
        }
        sessoes.append(sessao)

        print(f"  [{sessao['id']}] {usuario:8s} → {ponto} | "
              f"{potencia_max:5.1f} kW | "
              f"{inicio.strftime('%H:%M')}–{fim.strftime('%H:%M')} "
              f"({duracao_min} min)")

    print(f"\n  Total de sessões iniciadas: {len(sessoes)}")
    return sessoes


# ─────────────────────────────────────────────
# MÓDULO 02 — CÁLCULO DE CONSUMO
# ─────────────────────────────────────────────
def calcular_consumo(sessoes):
    """
    Calcula o consumo em kWh de cada sessão com base na potência
    alocada (após controle de demanda) e na duração da sessão.
    Também aplica a tarifa correta (pico ou normal) por horário.
    """
    separador("MÓDULO 02 — Cálculo de Consumo por Usuário")

    for sessao in sessoes:
        horas = sessao["duracao_min"] / 60.0
        kwh = sessao["potencia_alocada_kw"] * horas

        # Verifica se a sessão ocorre no horário de pico
        hora_inicio = sessao["inicio"].hour
        em_pico = HORA_PICO_INICIO <= hora_inicio < HORA_PICO_FIM
        tarifa = TARIFA_PICO if em_pico else TARIFA_NORMAL
        custo = kwh * tarifa

        sessao["kwh_consumido"] = round(kwh, 3)
        sessao["tarifa_aplicada"] = tarifa
        sessao["custo_brl"] = round(custo, 2)
        sessao["em_pico"] = em_pico

        pico_label = "⚡ PICO" if em_pico else "normal"
        print(f"  {sessao['usuario']:8s} | {sessao['ponto']} | "
              f"{kwh:.3f} kWh | "
              f"R$ {tarifa:.2f}/kWh ({pico_label}) | "
              f"Total: R$ {custo:.2f}")

    return sessoes


# ─────────────────────────────────────────────
# MÓDULO 03 — CONTROLE DE DEMANDA
# ─────────────────────────────────────────────
def controlar_demanda(sessoes):
    """
    Distribui a potência disponível entre os carregadores ativos,
    garantindo que a soma total não ultrapasse o limite contratado.

    Lógica:
      1. Calcula a demanda total solicitada.
      2. Se exceder o limite, aplica fator de redução proporcional.
      3. Atribui potência alocada a cada sessão.
    """
    separador("MÓDULO 03 — Controle de Demanda")

    demanda_total = sum(s["potencia_solicitada_kw"] for s in sessoes)
    print(f"  Demanda solicitada : {demanda_total:.1f} kW")
    print(f"  Limite contratado  : {LIMITE_DEMANDA_KW:.1f} kW")

    if demanda_total > LIMITE_DEMANDA_KW:
        fator = LIMITE_DEMANDA_KW / demanda_total
        print(f"  ⚠  Sobrecarga detectada! Fator de redução: {fator:.2%}")
        for s in sessoes:
            s["potencia_alocada_kw"] = round(s["potencia_solicitada_kw"] * fator, 2)
    else:
        fator = 1.0
        print(f"  ✔  Dentro do limite. Nenhum corte necessário.")
        for s in sessoes:
            s["potencia_alocada_kw"] = s["potencia_solicitada_kw"]

    demanda_alocada = sum(s["potencia_alocada_kw"] for s in sessoes)
    print(f"\n  {'Ponto':<10} {'Solicitado':>12} {'Alocado':>10}")
    print(f"  {'─'*35}")
    for s in sessoes:
        print(f"  {s['ponto']:<10} "
              f"{s['potencia_solicitada_kw']:>10.1f} kW "
              f"{s['potencia_alocada_kw']:>8.1f} kW")
    print(f"  {'─'*35}")
    print(f"  {'TOTAL':<10} {demanda_total:>10.1f} kW {demanda_alocada:>8.1f} kW")

    return sessoes


# ─────────────────────────────────────────────
# MÓDULO 04 — RELATÓRIO DE USO
# ─────────────────────────────────────────────
def gerar_relatorio(sessoes):
    """
    Consolida todas as sessões e gera um relatório operacional com:
      - Resumo por usuário (kWh, custo, ponto utilizado)
      - Totais do eletroposto (energia fornecida, receita, ocupação)
      - Recomendação de IA: melhor horário para recarga com menor custo
    """
    separador("MÓDULO 04 — Relatório de Uso e Receita")

    total_kwh  = 0.0
    total_brl  = 0.0

    print(f"\n  {'#':<3} {'Usuário':<10} {'Ponto':<10} "
          f"{'kWh':>7} {'Tarifa':>8} {'Custo':>9} {'Pico?':>6}")
    print(f"  {'─'*58}")

    for s in sessoes:
        total_kwh += s["kwh_consumido"]
        total_brl += s["custo_brl"]
        pico_label = "Sim" if s["em_pico"] else "Não"
        print(f"  {s['id']:<3} {s['usuario']:<10} {s['ponto']:<10} "
              f"{s['kwh_consumido']:>6.3f} "
              f"R${s['tarifa_aplicada']:>5.2f}/kWh "
              f"R${s['custo_brl']:>7.2f} "
              f"{pico_label:>6}")

    print(f"  {'─'*58}")
    print(f"  {'TOTAL':<24} {total_kwh:>6.3f} kWh {'':>14} R${total_brl:>7.2f}")

    ocupacao = (len(sessoes) / NUM_PONTOS) * 100
    separador()
    print(f"  Ocupação do eletroposto : {ocupacao:.0f}% ({len(sessoes)}/{NUM_PONTOS} pontos)")
    print(f"  Energia total fornecida : {total_kwh:.3f} kWh")
    print(f"  Receita total estimada  : R$ {total_brl:.2f}")

    # ── Recomendação de IA (lógica de orientação ao usuário) ──
    separador("IA — Orientação ao Usuário")
    economia = round((TARIFA_PICO - TARIFA_NORMAL) / TARIFA_PICO * 100, 1)
    print(f"\n  Análise de tarifação dinâmica:")
    print(f"    • Tarifa fora do pico : R$ {TARIFA_NORMAL:.2f}/kWh")
    print(f"    • Tarifa no pico      : R$ {TARIFA_PICO:.2f}/kWh")
    print(f"    • Economia potencial  : {economia}% ao evitar o pico")
    print(f"\n  Recomendação:")
    print(f"    Prefira carregar antes das {HORA_PICO_INICIO}h ou após as {HORA_PICO_FIM}h.")
    print(f"    Nos horários de pico ({HORA_PICO_INICIO}h–{HORA_PICO_FIM}h), a tarifa é")
    print(f"    {economia}% mais cara. Carregando 30 kWh fora do pico,")
    economia_valor = round(30 * (TARIFA_PICO - TARIFA_NORMAL), 2)
    print(f"    você economiza aproximadamente R$ {economia_valor:.2f} por sessão.")

    separador()
    print(f"\n  Simulação concluída em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"  ChargeGrid Intelligence — FIAP x GoodWe 2026\n")


# ─────────────────────────────────────────────
# EXECUÇÃO PRINCIPAL
# ─────────────────────────────────────────────
def main():
    print("\n" + "═" * 58)
    print("  CHARGEGRID INTELLIGENCE — Simulação do Eletroposto")
    print("  EV Challenge 2026 | FIAP x GoodWe | Grupo GTLF")
    print("═" * 58)

    # Módulo 01: gera sessões
    sessoes = simular_sessoes(num_sessoes=4)

    # Módulo 03: controla demanda antes de calcular consumo
    # (a potência alocada é necessária para o cálculo correto de kWh)
    sessoes = controlar_demanda(sessoes)

    # Módulo 02: calcula consumo com a potência já alocada
    sessoes = calcular_consumo(sessoes)

    # Módulo 04: relatório consolidado
    gerar_relatorio(sessoes)


if __name__ == "__main__":
    main()