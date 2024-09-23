from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "sparkit_secret_key"

# Função para conectar ao banco de dados SQLite
def get_db_connection():
    conn = sqlite3.connect('sparkit.db')
    conn.row_factory = sqlite3.Row
    return conn

# Rota da página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para a página de cadastro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        if not name or not email or not password:
            flash('Todos os campos são obrigatórios!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO customers (name, email, password) VALUES (?, ?, ?)', (name, email, password))
            conn.commit()
            conn.close()
            flash('Cadastro realizado com sucesso!')
            return redirect(url_for('index'))

    return render_template('register.html')

# Inicialização do banco de dados
def init_db():
    conn = get_db_connection()
    conn.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    ''')
    conn.close()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
