# Gulliver Back-End

from flask import Flask, render_template, request
import pymysql
import json

app = Flask(__name__)

# Configurazione connessione DB MySQL
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'password'
MYSQL_DB = 'gulliver'

# Connessione al DB
db = pymysql.connect(host = MYSQL_HOST, user = MYSQL_USER, password = MYSQL_PASSWORD, db = MYSQL_DB)

@app.route('/findTipologie?<nomeLuogo>', methods=['GET'])
def findAttivitaByTipologie(nomeLuogo):
    cursor = db.cursor()

    sql = 'select * from tipologie as t where t.nome = ' + nomeLuogo + ';'

    try:
        cursor.execute(sql)
        # Fetch tutti i dati in una lista di liste
        results = None
        results = cursor.fetchall()

        listaTipologie = []

        for row in results:
            id = row[0]
            nome = row[1]
            listaTipologie.append(Tipolgia(id, nome))

    except:
        print ("Error: unable to fecth data")

    return json.dumps(listaTipologie, default=vars)

@app.route("/logout")
def closeAll():
    db.close()

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000)
