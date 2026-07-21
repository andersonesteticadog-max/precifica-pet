def calcular_custo_servico(
    aluguel_mensal,
    agua_luz_mensal,
    dias_abertos_mes,
    horas_por_dia,
    valor_hora_funcionario,
    duracao_servico_min,
    custo_produtos_insumos,
    margem_lucro_desejada,
):
    """Calcula quanto um atendimento especifico custa de verdade pro negocio,
    e qual seria o preco minimo pra nao dar prejuizo.

    O custo fixo (aluguel + agua/luz) e' rateado proporcionalmente ao TEMPO
    que o servico ocupa da estrutura: um servico de 90min "usa" 3x mais a
    loja do que um de 30min, entao paga 3x mais fixo. Por isso dividimos o
    custo fixo mensal pelas horas totais que o negocio fica aberto no mes,
    e multiplicamos pela duracao deste servico especifico.
    """
    horas_operacao_mes = dias_abertos_mes * horas_por_dia
    custo_fixo_por_hora = (aluguel_mensal + agua_luz_mensal) / horas_operacao_mes

    duracao_horas = duracao_servico_min / 60
    custo_fixo_rateado = custo_fixo_por_hora * duracao_horas
    custo_mao_de_obra = valor_hora_funcionario * duracao_horas

    custo_total = custo_fixo_rateado + custo_mao_de_obra + custo_produtos_insumos
    preco_minimo_sugerido = custo_total * (1 + margem_lucro_desejada)

    return {
        "custo_fixo_rateado": round(custo_fixo_rateado, 2),
        "custo_mao_de_obra": round(custo_mao_de_obra, 2),
        "custo_produtos_insumos": round(custo_produtos_insumos, 2),
        "custo_total": round(custo_total, 2),
        "preco_minimo_sugerido": round(preco_minimo_sugerido, 2),
    }
