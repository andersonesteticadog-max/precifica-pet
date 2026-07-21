import sys
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "src")

from precificapet.calculo import calcular_custo_servico


def pedir_numero(pergunta):
    while True:
        texto = input(pergunta).strip().replace(",", ".")
        try:
            return float(texto)
        except ValueError:
            print("Digite um numero valido.\n")


def main():
    print("=== PrecificaPet (modo teste) ===\n")
    print("-- Custos fixos do negocio (mensais) --")
    aluguel = pedir_numero("Aluguel mensal (R$): ")
    agua_luz = pedir_numero("Agua + luz mensal (R$): ")
    dias_abertos = pedir_numero("Dias abertos por mes: ")
    horas_por_dia = pedir_numero("Horas de funcionamento por dia: ")

    print("\n-- Este servico especifico --")
    valor_hora_funcionario = pedir_numero("Custo por hora do funcionario (R$): ")
    duracao_min = pedir_numero("Duracao do servico (minutos): ")
    custo_produtos = pedir_numero("Custo de produtos/insumos usados (shampoo, algodao, etc) (R$): ")
    margem = pedir_numero("Margem de lucro desejada (ex: 0.30 para 30%): ")

    resultado = calcular_custo_servico(
        aluguel_mensal=aluguel,
        agua_luz_mensal=agua_luz,
        dias_abertos_mes=dias_abertos,
        horas_por_dia=horas_por_dia,
        valor_hora_funcionario=valor_hora_funcionario,
        duracao_servico_min=duracao_min,
        custo_produtos_insumos=custo_produtos,
        margem_lucro_desejada=margem,
    )

    print("\n=== Resultado ===")
    print(f"Custo fixo rateado (aluguel/agua/luz): R$ {resultado['custo_fixo_rateado']:.2f}")
    print(f"Custo de mao de obra:                  R$ {resultado['custo_mao_de_obra']:.2f}")
    print(f"Custo de produtos/insumos:              R$ {resultado['custo_produtos_insumos']:.2f}")
    print(f"CUSTO TOTAL do atendimento:             R$ {resultado['custo_total']:.2f}")
    print(f"PRECO MINIMO sugerido:                  R$ {resultado['preco_minimo_sugerido']:.2f}")


if __name__ == "__main__":
    main()
