import tornado.web
import tornado.ioloop
import sqlite3


# ----------------------------
# Função de conexão com o banco
# ----------------------------
def conexao_db(query, valores=()):
    conexao = sqlite3.connect("db/db.sqlite3")
    cursor = conexao.cursor()

    try:
        cursor.execute(query, valores)
        resultado = cursor.fetchall()
        conexao.commit()
    except Exception as erro:
        raise erro

    conexao.close()
    return resultado


# ----------------------------
# LOGIN
# ----------------------------
class Login(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/login.html")

    def post(self):
        usuario = self.get_argument("usuario")
        senha = self.get_argument("senha")

        query = "SELECT * FROM usuario WHERE nome=? AND senha=?"
        valores = (usuario, senha)
        resultado = conexao_db(query, valores)

        if resultado:
            self.redirect("/index")
        else:
            self.write("Usuário ou senha incorretos.")


# ----------------------------
# INDEX (página após login)
# ----------------------------
class Index(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/index.html")


# ----------------------------
# CRUD – CREATE
# ----------------------------
class UsuarioCreate(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/create.html")

    def post(self):
        nome = self.get_argument("nome")
        senha = self.get_argument("senha")

        query = "INSERT INTO usuario (nome, senha) VALUES (?, ?)"
        valores = (nome, senha)
        conexao_db(query, valores)

        self.write("Usuário criado! <br><a href='/usuario/list'>Ver usuários</a>")


# ----------------------------
# CRUD – READ
# ----------------------------
class UsuarioList(tornado.web.RequestHandler):
    def get(self):
        query = "SELECT id, nome, senha FROM usuario"
        usuarios = conexao_db(query)

        self.render("templates/list.html", usuarios=usuarios)


# ----------------------------
# CRUD – UPDATE
# ----------------------------
class UsuarioUpdate(tornado.web.RequestHandler):
    def get(self):
        user_id = self.get_argument("id")  # pega o ?id=3
        user = conexao_db("SELECT * FROM usuario WHERE id=?", (user_id,))
        self.render("templates/update.html", usuario=user[0])

    def post(self):
        id_user = self.get_argument("id")
        novo_nome = self.get_argument("nome")
        nova_senha = self.get_argument("senha")

        query = "UPDATE usuario SET nome=?, senha=? WHERE id=?"
        valores = (novo_nome, nova_senha, id_user)
        conexao_db(query, valores)

        self.write("Usuário atualizado! <br><a href='/usuario/list'>Voltar</a>")



# ----------------------------
# CRUD – DELETE
# ----------------------------
class UsuarioDelete(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/delete.html")

    def post(self):
        id_user = self.get_argument("id")

        query = "DELETE FROM usuario WHERE id=?"
        valores = (id_user,)
        conexao_db(query, valores)

        self.write("Usuário deletado! <br><a href='/usuario/list'>Voltar</a>")


# ----------------------------
# ROTAS
# ----------------------------
app = tornado.web.Application([
    (r"/", Login),
    (r"/index", Index),
    (r"/usuario/create", UsuarioCreate),
    (r"/usuario/list", UsuarioList),
    (r"/usuario/update", UsuarioUpdate),
    (r"/usuario/delete", UsuarioDelete),
    (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "static"}),
])


# ----------------------------
# INICIAR SERVIDOR
# ----------------------------
if __name__ == "__main__":
    app.listen(8888)
    print("Servidor rodando em: http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()
