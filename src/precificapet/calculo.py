def calcular_todos(config, servicos):
    """Calcula os indicadores de cada servico cadastrado.

    config: dict com aluguel_mensal, agua_luz_mensal, valor_hora_funcionario,
    margem_lucro_desejada (compartilhados por todo o salao).

    servicos: lista de dicts, cada um com nome, duracao_min,
    custo_produtos_insumos, preco_praticado e quantidade_atual_mes
    (quantos atendimentos desse tipo o salao faz por mes hoje).

    O custo fixo (aluguel + agua/luz) e' rateado proporcionalmente ao TEMPO
    que cada servico ocupa da estrutura: primeiro somamos as horas totais
    de atendimento do salao inteiro no mes (juntando todos os tipos), daí
    cada servico paga a fatia do fixo correspondente as horas que ele
    ocupa. Um servico que demora mais paga proporcionalmente mais.

    Alem do custo, calcula a QUANTIDADE MINIMA e o FATURAMENTO MINIMO
    daquele tipo de servico - ou seja, se o salao vivesse so daquele
    servico, quantas vendas por mes seriam necessarias pra cobrir o custo
    fixo total do negocio e ainda bater a margem de lucro desejada. Isso
    usa o preco praticado (o que voce cobra) e a margem de contribuicao
    (preco menos o custo variavel direto do servico).
    """
    custo_fixo_mensal = config["aluguel_mensal"] + config["agua_luz_mensal"]
    horas_totais_mes = sum(
        s["quantidade_atual_mes"] * (s["duracao_min"] / 60) for s in servicos
    )
    custo_fixo_por_hora = custo_fixo_mensal / horas_totais_mes if horas_totais_mes else 0

    resultados = []
    for s in servicos:
        duracao_horas = s["duracao_min"] / 60
        custo_fixo_rateado = custo_fixo_por_hora * duracao_horas
        custo_mao_de_obra = config["valor_hora_funcionario"] * duracao_horas
        custo_variavel_direto = custo_mao_de_obra + s["custo_produtos_insumos"]

        custo_total = custo_fixo_rateado + custo_variavel_direto
        preco_minimo_sugerido = custo_total * (1 + config["margem_lucro_desejada"])

        margem_contribuicao = s["preco_praticado"] - custo_variavel_direto
        if margem_contribuicao > 0:
            quantidade_minima = (
                custo_fixo_mensal * (1 + config["margem_lucro_desejada"]) / margem_contribuicao
            )
            faturamento_minimo = quantidade_minima * s["preco_praticado"]
        else:
            # O preco praticado nem cobre o custo variavel direto do
            # servico (mao de obra + produtos) - vender mais unidades so
            # aumenta o prejuizo, nao existe "quantidade minima" possivel.
            quantidade_minima = None
            faturamento_minimo = None

        resultados.append({
            **s,
            "custo_fixo_rateado": round(custo_fixo_rateado, 2),
            "custo_mao_de_obra": round(custo_mao_de_obra, 2),
            "custo_total": round(custo_total, 2),
            "preco_minimo_sugerido": round(preco_minimo_sugerido, 2),
            "quantidade_minima": (
                round(quantidade_minima, 1) if quantidade_minima is not None else None
            ),
            "faturamento_minimo": (
                round(faturamento_minimo, 2) if faturamento_minimo is not None else None
            ),
        })

    return resultados
