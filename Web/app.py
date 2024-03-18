from flask import Flask, request, render_template
#import json
import pymysql

appWebApi = Flask(__name__)

#Connessione al db con pymysql (pip install pymysql    --   import pymysql)
db = pymysql.connect(host="127.0.0.1", user="root", password="NUOVAPASSWORD", db="gulliver")

class Tipologie:
    nome_itinerario = None
    nome_categoria = None

    def __init__(self, ni, nc):
        self.nome_itinerario = ni
        self.nome_categoria = nc


@appWebApi.route("/home")
def main():
    return render_template('home.html')


@appWebApi.route("/ideemontagna")
def getIdeeMontagnaByDB():
    cursor = db.cursor()
    sql = "SELECT i.nome AS nome_itinerario, c.nome AS nome_categoria \
            FROM itinerari i \
            JOIN attivita_itinerari ai ON i.ID = ai.id_itinerario\
            JOIN attivita_luoghi al ON ai.id_attivita = al.id_attivita\
            JOIN luoghi l ON al.id_luogo = l.ID\
            JOIN luoghi_categorie lc ON l.ID = lc.id_luogo\
            JOIN categorie c ON lc.id_categoria = c.ID\
            Where c.ID = 1;"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        listaItinerariXCategoria = []
        for row in results:
            nome_itinerario = row[0]
            nome_categoria = row[1]
            #print ("nome_itinerario=%s, nome_categoria=%s" % \
            #      (nome_itinerario, nome_categoria))
            listaItinerariXCategoria.append(Tipologie(nome_itinerario, nome_categoria))
    except:
        print ("Error: cannot fetch data")
    return render_template("idee_montagna.html", categoria = nome_categoria, lista = listaItinerariXCategoria)


@appWebApi.route("/ideemare")
def getIdeeMareByDB():
    cursor = db.cursor()
    sql = "SELECT i.nome AS nome_itinerario, c.nome AS nome_categoria \
            FROM itinerari i \
            JOIN attivita_itinerari ai ON i.ID = ai.id_itinerario\
            JOIN attivita_luoghi al ON ai.id_attivita = al.id_attivita\
            JOIN luoghi l ON al.id_luogo = l.ID\
            JOIN luoghi_categorie lc ON l.ID = lc.id_luogo\
            JOIN categorie c ON lc.id_categoria = c.ID\
            Where c.ID = 2;"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        listaItinerariXCategoria = []
        for row in results:
            nome_itinerario = row[0]
            nome_categoria = row[1]
            #print ("nome_itinerario=%s, nome_categoria=%s" % \
            #       (nome_itinerario, nome_categoria))
            listaItinerariXCategoria.append(Tipologie(nome_itinerario, nome_categoria))
    except:
        print ("Error: cannot fetch data")
    return render_template('idee_mare.html',  categoria = nome_categoria, lista = listaItinerariXCategoria)


@appWebApi.route("/ideecitta")
def getIdeeCittaByDB():
    cursor = db.cursor()
    sql = "SELECT i.nome AS nome_itinerario, c.nome AS nome_categoria \
            FROM itinerari i \
            JOIN attivita_itinerari ai ON i.ID = ai.id_itinerario\
            JOIN attivita_luoghi al ON ai.id_attivita = al.id_attivita\
            JOIN luoghi l ON al.id_luogo = l.ID\
            JOIN luoghi_categorie lc ON l.ID = lc.id_luogo\
            JOIN categorie c ON lc.id_categoria = c.ID\
            Where c.ID = 3;"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        listaItinerariXCategoria = []
        for row in results:
            nome_itinerario = row[0]
            nome_categoria = row[1]
            listaItinerariXCategoria.append(Tipologie(nome_itinerario, nome_categoria))
            #print ("nome_itinerario=%s, nome_categoria=%s" % \
            #       (nome_itinerario, nome_categoria))
    except:
        print ("Error: cannot fetch data")
    return render_template('idee_citta.html',  categoria = nome_categoria, lista = listaItinerariXCategoria)











if __name__ == "__main__":
    appWebApi.run(host='0.0.0.0', port=5000)







