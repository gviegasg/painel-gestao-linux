import datetime
import sqlite3


class SistemaAnalise:

    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.criar_tabela()

    def criar_tabela(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs_acesso (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT NOT NULL,
                evento TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def registrar_evento(self, mensagem):
        data_atual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute(
            "INSERT INTO logs_acesso (data, evento) VALUES (?, ?)",
            (data_atual, mensagem),
        )
        self.conn.commit()
        print(f"✅ Evento registrado no banco SQLite: '{mensagem}' às {data_atual}")

    def listar_logs(self):
        self.cursor.execute(
            "SELECT * FROM logs_acesso ORDER BY id DESC LIMIT 5"
        )
        registros = self.cursor.fetchall()
        print("\n📋 Últimos 5 logs registrados:")
        for reg in registros:
            print(f"   ID: {reg[0]} | Data: {reg[1]} | Evento: {reg[2]}")

    def fechar(self):
        self.conn.close()


if __name__ == "__main__":
    db_file = "/home/gviegasg/.scripts/projeto_ads/database.db"
    app = SistemaAnalise(db_file)
    app.registrar_evento("Execução manual via Módulo ADS")
    app.listar_logs()
    app.fechar()
