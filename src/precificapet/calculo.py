def calcular_custo_servico(
    aluguel_mensal,
    agua_luz_mensal,
    quantidade_atendimentos_mes,
    valor_hora_funcionario,
    duracao_servico_min,
    custo_produtos_insumos,
    margem_lucro_desejada,
):
    """Calcula quanto um atendimento especifico custa de verdade pro negocio,
    e qual seria o preco minimo pra nao dar prejuizo.

    O custo fixo (aluguel + agua/luz) e' dividido pela quantidade de
    atendimentos REALMENTE feitos no mes (nao pelas horas que a loja fica
    de portas abertas) - um salao mais vazio precisa que cada atendimento
    pague uma fatia maior do aluguel, um salao mais cheio dilui melhor esse
    custo. Com um unico tipo de servico na conta (ainda sem o cadastro de
    varios tipos), isso vira uma divisao simples; a ponderacao por duracao
    volta a fazer diferenca quando houver mais de um tipo de servico pra
    comparar entre si.
    """
    custo_fixo_rateado = (aluguel_mensal + agua_luz_mensal) / quantidade_atendimentos_mes

    duracao_horas = duracao_servico_min / 60
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
