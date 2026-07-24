import sqlite3

DB_PATH = "precificapet.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS configuracao (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    aluguel_mensal REAL NOT NULL,
    agua_luz_mensal REAL NOT NULL,
    valor_hora_funcionario REAL NOT NULL,
    margem_lucro_desejada REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS servicos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    duracao_min REAL NOT NULL,
    custo_produtos_insumos REAL NOT NULL,
    preco_praticado REAL NOT NULL,
    quantidade_atual_mes REAL NOT NULL
);
"""


def conectar():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def inicializar():
    conn = conectar()
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()


def obter_configuracao():
    conn = conectar()
    linha = conn.execute("SELECT * FROM configuracao WHERE id = 1").fetchone()
    conn.close()
    return dict(linha) if linha else None


def salvar_configuracao(aluguel_mensal, agua_luz_mensal, valor_hora_funcionario, margem_lucro_desejada):
    conn = conectar()
    conn.execute(
        "INSERT INTO configuracao (id, aluguel_mensal, agua_luz_mensal, valor_hora_funcionario, "
        "margem_lucro_desejada) VALUES (1, ?, ?, ?, ?) "
        "ON CONFLICT(id) DO UPDATE SET aluguel_mensal = excluded.aluguel_mensal, "
        "agua_luz_mensal = excluded.agua_luz_mensal, "
        "valor_hora_funcionario = excluded.valor_hora_funcionario, "
        "margem_lucro_desejada = excluded.margem_lucro_desejada",
        (aluguel_mensal, agua_luz_mensal, valor_hora_funcionario, margem_lucro_desejada),
    )
    conn.commit()
    conn.close()


def listar_servicos():
    conn = conectar()
    linhas = conn.execute("SELECT * FROM servicos ORDER BY id").fetchall()
    conn.close()
    return [dict(linha) for linha in linhas]


def adicionar_servico(nome, duracao_min, custo_produtos_insumos, preco_praticado, quantidade_atual_mes):
    conn = conectar()
    conn.execute(
        "INSERT INTO servicos (nome, duracao_min, custo_produtos_insumos, preco_praticado, "
        "quantidade_atual_mes) VALUES (?, ?, ?, ?, ?)",
        (nome, duracao_min, custo_produtos_insumos, preco_praticado, quantidade_atual_mes),
    )
    conn.commit()
    conn.close()


def excluir_servico(servico_id):
    conn = conectar()
    conn.execute("DELETE FROM servicos WHERE id = ?", (servico_id,))
    conn.commit()
    conn.close()
