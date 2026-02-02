import sqlite3


class BancoDados:
    SALDO_INICIAL = 20

    def __init__(self):
        self.conn = sqlite3.connect("haze_bot.db")
        self.cursor = self.conn.cursor()
        self.criar_tabela()

    def criar_tabela(self):
        self.cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS usuarios (
                user_id INTEGER PRIMARY KEY,
                hazium INTEGER DEFAULT {self.SALDO_INICIAL}
            )
        """
        )
        self.conn.commit()

    def alterar_hazium(self, user_id, quantidade):
        # Garante que cria com 20 se não existir
        self.cursor.execute(
            f"INSERT OR IGNORE INTO usuarios (user_id, hazium) VALUES (?, {self.SALDO_INICIAL})",
            (user_id,),
        )

        self.cursor.execute(
            "UPDATE usuarios SET hazium = hazium + ? WHERE user_id = ?",
            (quantidade, user_id),
        )
        self.conn.commit()

    def ver_saldo(self, user_id):
        self.cursor.execute("SELECT hazium FROM usuarios WHERE user_id = ?", (user_id,))
        resultado = self.cursor.fetchone()

        # AQUI ESTAVA O ERRO: Agora retorna 20 se o cara não existir
        return resultado[0] if resultado else self.SALDO_INICIAL

    def pegar_ranking(self):
        self.cursor.execute(
            "SELECT user_id, hazium FROM usuarios ORDER BY hazium DESC LIMIT 10"
        )
        return self.cursor.fetchall()


db = BancoDados()
