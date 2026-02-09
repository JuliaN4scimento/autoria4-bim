from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import os 
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "mitoverso123"

# PASTA ONDE AS IMAGENS SERÃO SALVAS
UPLOAD_FOLDER = "static/img"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# CONEXÃO COM O BANCO
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="infoj",
        database="mitoverso"
    )

# PÁGINA INICIAL
@app.route("/")
def index():
    return render_template("index.html")

# PERSONAGENS
@app.route("/linha_tempo")
def linha_tempo():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM personagens ORDER BY id DESC")
    personagens = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("telaprincipal.html", personagens=personagens)

# ADICIONAR PERSONAGEM (SÓ LOGADO)
@app.route("/add_personagem", methods=["POST"])
def add_personagem():

    if "usuario_id" not in session:
        return redirect(url_for("login"))

    nome = request.form["nome"]
    descricao = request.form["descricao"]

    # UPLOAD DA IMAGEM PELO PC
    imagem = request.files["imagem"]
    nome_arquivo = secure_filename(imagem.filename)

    caminho = os.path.join(app.config["UPLOAD_FOLDER"], nome_arquivo)
    imagem.save(caminho)

    # SALVAR NO BANCO
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO personagens (nome, descricao, imagem) VALUES (%s, %s, %s)",
        (nome, descricao, nome_arquivo)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for("linha_tempo"))

# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM usuarios WHERE email=%s AND senha=%s",
            (email, senha)
        )

        usuario = cursor.fetchone()

        cursor.close()
        conn.close()

        if usuario:
            # salva na sessão
            session["usuario_id"] = usuario["id"]
            session["email"] = usuario["email"]

            # volta para linha do tempo
            return redirect(url_for("linha_tempo"))

        return render_template("login.html", erro="Email ou senha inválidos")

    return render_template("login.html")

# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("linha_tempo"))

# CADASTRO
@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO usuarios (email, senha) VALUES (%s, %s)",
                (email, senha)
            )
            conn.commit()

        except:
            return "Erro ao cadastrar usuário"

        cursor.close()
        conn.close()

        return redirect(url_for("login"))

    return render_template("cadastro.html")

# EXCLUIR PERSONAGEM
@app.route("/excluir/<int:id>")
def excluir_personagem(id):

    # Só permite excluir se estiver logado
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM personagens WHERE id = %s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("linha_tempo"))

#EDITAR PERSONAGEM
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_personagem(id):

    # Só permite editar se estiver logado
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Buscar personagem atual
    cursor.execute("SELECT * FROM personagens WHERE id = %s", (id,))
    personagem = cursor.fetchone()

    # Se enviar o formulário (POST)
    if request.method == "POST":
        nome = request.form["nome"]
        descricao = request.form["descricao"]

        cursor.execute("""
            UPDATE personagens
            SET nome = %s, descricao = %s
            WHERE id = %s
        """, (nome, descricao, id))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("linha_tempo"))

    cursor.close()
    conn.close()

    return render_template("editar.html", personagem=personagem)

# PÁGINAS INFORMATIVAS
@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

@app.route("/referencias")
def referencias():
    return render_template("referencias.html")

@app.route("/academico")
def academico():
    return render_template("academico.html")

# EXECUÇÃO
if __name__ == "__main__":
    app.run(debug=True)