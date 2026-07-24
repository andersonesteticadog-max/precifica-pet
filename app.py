import sys
sys.path.insert(0, "src")

from flask import Flask, render_template, request

from precificapet.calculo import calcular_custo_servico

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    if request.method == "POST":
        resultado = calcular_custo_servico(
            aluguel_mensal=float(request.form["aluguel_mensal"]),
            agua_luz_mensal=float(request.form["agua_luz_mensal"]),
            quantidade_atendimentos_mes=float(request.form["quantidade_atendimentos_mes"]),
            valor_hora_funcionario=float(request.form["valor_hora_funcionario"]),
            duracao_servico_min=float(request.form["duracao_servico_min"]),
            custo_produtos_insumos=float(request.form["custo_produtos_insumos"]),
            margem_lucro_desejada=float(request.form["margem_lucro_desejada"]),
        )
    return render_template("index.html", resultado=resultado)


if __name__ == "__main__":
    app.run(debug=True)
