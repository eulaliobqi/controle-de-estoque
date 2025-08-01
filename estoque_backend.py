import sqlite3

class EstoqueDB:
    def __init__(self, db_name="estoque.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        self.conn.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            referencia TEXT,
            categoria TEXT,
            nome TEXT NOT NULL,
            ncm TEXT,
            volume TEXT,
            quantidade INTEGER
        )
        ''')

    def cadastrar_produto(self, ref, cat, nome, ncm, vol, qtd):
        self.conn.execute('''
            INSERT INTO produtos (referencia, categoria, nome, ncm, volume, quantidade)
            VALUES (?, ?, ?, ?, ?, ?)''', (ref, cat, nome, ncm, vol, qtd))
        self.conn.commit()

    def entrada_produto(self, nome, qtd):
        self.conn.execute("UPDATE produtos SET quantidade = quantidade + ? WHERE nome = ?", (qtd, nome))
        self.conn.commit()

    def saida_produto(self, nome, qtd):
        self.conn.execute("UPDATE produtos SET quantidade = quantidade - ? WHERE nome = ? AND quantidade >= ?",
                          (qtd, nome, qtd))
        self.conn.commit()

    def listar_produtos(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT referencia, categoria, nome, ncm, volume, quantidade FROM produtos")
        return cursor.fetchall()

    def fechar_conexao(self):
        self.conn.close()
