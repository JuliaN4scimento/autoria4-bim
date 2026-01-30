from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="infoj",
        database="mitoverso"
    )

# Página inicial
@app.route("/")
def index():
    return render_template("index.html")

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = int(request.form["senha"])  # senha INT

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM usuarios WHERE email = %s AND senha = %s",
            (email, senha)
        )

        usuario = cursor.fetchone()

        cursor.close()
        conn.close()

        if usuario:
            return redirect(url_for("telaprincipal"))
        else:
            return "Email ou senha inválidos"

    return render_template("login.html")

# Cadastro
@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        email = request.form["email"]
        senha = int(request.form["senha"])

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO usuarios (email, senha) VALUES (%s, %s)",
                (email, senha)
            )
            conn.commit()
        except mysql.connector.Error as err:
            cursor.close()
            conn.close()
            return "Erro ao cadastrar usuário"

        cursor.close()
        conn.close()

        return redirect(url_for("login"))

    return render_template("cadastro.html")

# Tela principal
@app.route("/telaprincipal")
def telaprincipal():
    return render_template("telaprincipal.html")

# Páginas informativas
@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

@app.route("/referencias")
def referencias():
    return render_template("referencias.html")

@app.route("/academico")
def academico():
    return render_template("academico.html")

if __name__ == "__main__":
    app.run(debug=True)