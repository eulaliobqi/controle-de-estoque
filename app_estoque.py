import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
from estoque_backend import EstoqueDB

db = EstoqueDB()

class EstoqueApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Sistema de Estoque Inteligente")
        self.master.geometry("1100x700")

        # ---------- Título ----------
        tb.Label(master, text="Cadastro de Produtos", font=("Helvetica", 18, "bold")).pack(pady=10)

        # ---------- Frame de Cadastro Centralizado ----------
        frame_container = tb.Frame(master)
        frame_container.pack(pady=10)

        frame_form = tb.Frame(frame_container)
        frame_form.pack()

        self.entries = {}
        campos = [("Referência", "referencia"), ("Categoria", "categoria"), ("Nome", "nome"),
                  ("NCM/SH", "ncm"), ("Volume", "volume"), ("Quantidade", "quantidade")]

        for i, (label_text, key) in enumerate(campos):
            subframe = tb.Frame(frame_form)
            subframe.grid(row=0, column=i, padx=(5 if i == 0 else 15), sticky="n")

            # Label e Entry com fonte aumentada
            tb.Label(subframe, text=label_text, font=("Segoe UI", 11, "bold")).pack(anchor=CENTER)
            entry = tb.Entry(subframe, width=14, font=("Segoe UI", 11))
            entry.pack()

            # Linha divisora entre colunas (exceto último)
            if i < len(campos) - 1:
                tb.Separator(frame_form, orient=VERTICAL).grid(row=0, column=i + 1, sticky="ns", padx=3)
            self.entries[key] = entry

        tb.Button(master, text="Cadastrar Produto", bootstyle="success", command=self.cadastrar, width=25).pack(pady=10)

        # ---------- Frame de Movimentação ----------
        frame_mov = tb.LabelFrame(master, text="Movimentação de Estoque", padding=10)
        frame_mov.pack(pady=10, padx=20, fill=X)

        tb.Label(frame_mov, text="Produto:", font=("Segoe UI", 10)).grid(row=0, column=0, padx=5, sticky=W)
        self.produto_var = tb.StringVar()
        self.produto_combo = tb.Combobox(frame_mov, textvariable=self.produto_var, width=30)
        self.produto_combo.grid(row=0, column=1, padx=5)

        tb.Label(frame_mov, text="Quantidade:", font=("Segoe UI", 10)).grid(row=0, column=2, padx=5, sticky=W)
        self.qtd_mov = tb.Entry(frame_mov, width=10)
        self.qtd_mov.grid(row=0, column=3, padx=5)

        tb.Button(frame_mov, text="Entrada", bootstyle="info", command=self.entrada).grid(row=0, column=4, padx=5)
        tb.Button(frame_mov, text="Saída", bootstyle="warning", command=self.saida).grid(row=0, column=5, padx=5)

        # ---------- Tabela ----------
        self.frame_tabela = tb.Frame(master)
        self.frame_tabela.pack(fill=BOTH, expand=True, padx=20, pady=10)

        style = tb.Style()
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        style.configure("Treeview", rowheight=30, font=("Segoe UI", 10))

        self.tree = tb.Treeview(self.frame_tabela, columns=(
            "Referência", "Categoria", "Nome", "NCM/SH", "Volume", "Quantidade"),
            show="headings", style="Treeview")

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=180)

        vsb = tb.Scrollbar(self.frame_tabela, orient="vertical", command=self.tree.yview)
        hsb = tb.Scrollbar(self.frame_tabela, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        self.frame_tabela.grid_rowconfigure(0, weight=1)
        self.frame_tabela.grid_columnconfigure(0, weight=1)

        self.atualizar_tabela()

    # ---------- Funções ----------
    def cadastrar(self):
        try:
            dados = {k: self.entries[k].get() for k in self.entries}
            dados["quantidade"] = int(dados["quantidade"])
            db.cadastrar_produto(dados["referencia"], dados["categoria"], dados["nome"],
                                 dados["ncm"], dados["volume"], dados["quantidade"])
            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
            self.atualizar_tabela()
            for e in self.entries.values():
                e.delete(0, 'end')
        except ValueError:
            messagebox.showerror("Erro", "Quantidade deve ser um número inteiro!")

    def entrada(self):
        nome = self.produto_var.get()
        try:
            qtd = int(self.qtd_mov.get())
            db.entrada_produto(nome, qtd)
            self.atualizar_tabela()
            self.qtd_mov.delete(0, 'end')
        except ValueError:
            messagebox.showerror("Erro", "Quantidade inválida!")

    def saida(self):
        nome = self.produto_var.get()
        try:
            qtd = int(self.qtd_mov.get())
            db.saida_produto(nome, qtd)
            self.atualizar_tabela()
            self.qtd_mov.delete(0, 'end')
        except ValueError:
            messagebox.showerror("Erro", "Quantidade inválida!")

    def atualizar_tabela(self):
        self.tree.delete(*self.tree.get_children())
        produtos = db.listar_produtos()
        for row in produtos:
            self.tree.insert("", "end", values=row)

        nomes_produtos = [row[2] for row in produtos]
        self.produto_combo['values'] = nomes_produtos


if __name__ == "__main__":
    app = tb.Window(themename="superhero")  # temas: cosmo, minty, flatly, morph, superhero
    EstoqueApp(app)
    app.mainloop()
