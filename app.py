import sys
sys.path.insert(0, "src")

from flask import Flask, redirect, render_template, request, url_for

from precificapet import db
from precificapet.calculo import calcular_todos

app = Flask(__name__)
db.inicializar()


@app.route("/")
def index():
    config = db.obter_configuracao()
    servicos = db.listar_servicos()
    resultados = calcular_todos(config, servicos) if config else []
    return render_template("index.html", config=config, resultados=resultados)


@app.route("/configuracao", methods=["POST"])
def salvar_configuracao():
    db.salvar_configuracao(
        aluguel_mensal=float(request.form["aluguel_mensal"]),
        agua_luz_mensal=float(request.form["agua_luz_mensal"]),
        valor_hora_funcionario=float(request.form["valor_hora_funcionario"]),
        margem_lucro_desejada=float(request.form["margem_lucro_desejada"]),
    )
    return redirect(url_for("index"))


@app.route("/servicos", methods=["POST"])
def adicionar_servico():
    db.adicionar_servico(
        nome=request.form["nome"],
        duracao_min=float(request.form["duracao_min"]),
        custo_produtos_insumos=float(request.form["custo_produtos_insumos"]),
        preco_praticado=float(request.form["preco_praticado"]),
        quantidade_atual_mes=float(request.form["quantidade_atual_mes"]),
    )
    return redirect(url_for("index"))


@app.route("/servicos/<int:servico_id>/excluir", methods=["POST"])
def excluir_servico(servico_id):
    db.excluir_servico(servico_id)
    return redirect(url_for("index"))


if __name__ == "__main__":
    # use_reloader=False: o reloader do Flask sobe um processo "pai" que fica
    # de olho nos arquivos e um "filho" que roda o site de verdade - matar so
    # um dos dois faz o outro continuar vivo, e isso estava deixando processos
    # travados na porta 5000 entre testes. Sem o reloader, precisa reiniciar
    # manualmente apos mudar o codigo Python (templates continuam recarregando
    # sozinhos, isso nao muda).
    app.run(debug=True, use_reloader=False)
