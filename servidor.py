import tornado
import sqlite3

def conexao_db(query,valores):
        print(query)
        conexao = sqlite3.connect("db/db.sqlite3")
        cursor= conexao.cursor()
        try:
            cursor.execute(query,valores)
            resultado = cursor.fetchall()
            conexao.commit()
        except Exception:
                raise
        conexao.close()
        return resultado

class Login(tornado.web.RequestHandler):

    def get(self):
        self.render("templates/login.html")

    def post(self):
        usuario = self.get_argument("usuario")
        senha = self.get_argument("senha")
        query = "SELECT * FROM usuario WHERE nome=? AND senha=?"
        valores = (usuario,senha)
        resultado = conexao_db(query,valores)
        if resultado:
            self.render("templates/index.html")
        else:
            self.write("Usuário ou senha não encontrados.")


# cria as rotas
app = tornado.web.Application([
         (r"/", Login),
         ])

if __name__ == "__main__":
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()