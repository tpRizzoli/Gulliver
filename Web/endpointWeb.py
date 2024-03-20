from flask import Flask, request, render_template
import pymysql
import json

appWebApi = Flask(__name__)

# Configurazione connessione DB MySQL
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'NUOVAPASSWORD'
MYSQL_DB = 'gulliver'



# Connessione al DB
db = pymysql.connect(host = MYSQL_HOST, user = MYSQL_USER, password = MYSQL_PASSWORD, db = MYSQL_DB)



class Categoria:
    nome_itinerario = None
    nome_categoria = None
    def __init__(self, ni, nc):
        self.nome_itinerario = ni
        self.nome_categoria = nc

class Tipologia:
    id_tipologia = None
    nome_tipologia =None
    def __init__(self, id, nt):
        self.id_tipologia = id
        self.nome_tipologia = nt



@appWebApi.route("/")
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
            listaItinerariXCategoria.append(Categoria(nome_itinerario, nome_categoria))
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
            listaItinerariXCategoria.append(Categoria(nome_itinerario, nome_categoria))
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
            listaItinerariXCategoria.append(Categoria(nome_itinerario, nome_categoria))
            #print ("nome_itinerario=%s, nome_categoria=%s" % \
            #       (nome_itinerario, nome_categoria))
    except:
        print ("Error: cannot fetch data")
    return render_template('idee_citta.html',  categoria = nome_categoria, lista = listaItinerariXCategoria)


#GET http://localhost:5000/?destinazione=
@appWebApi.route("/destinazione") 
def getTipologieAttivita():
    nomeLuogo = str(request.args.get('destinazione'))

    cursor = db.cursor()
    sql = "SELECT t.ID AS id_tipologia, t.nome AS nome_tipologia\
        FROM luoghi l\
        JOIN attivita_luoghi al ON l.ID = al.id_luogo\
        JOIN attivita a ON al.id_attivita = a.ID\
        JOIN tipologie t ON a.id_tipologia = t.ID\
        WHERE l.nome ="+nomeLuogo+";"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        listaTipologieXLuogo = []
        for row in results:
            id_tipologia = row[0]
            nome_tipologia = row[1]
            listaTipologieXLuogo.append(Tipologia(id_tipologia, nome_tipologia))
    except:
        print ("Error: cannot fetch data")
    return render_template('sceltaTipologia.html', tipologia = nome_tipologia, lista = listaTipologieXLuogo)

   










#--------------------------------------------------------------------------------------------------------------------------------
# Classi database
# class Attivita:
#     def __init__(self, id, nome, tipologia, difficolta, descrizione):
#         self.id = id
#         self.nome = nome
#         self.tipologia = tipologia
#         self.difficolta = difficolta
#         self.descrizione = descrizione

# class Utente:
#     def __init__(self, id, username, email, password):
#         self.id = id
#         self.username = username
#         self.email = email
#         self.password = password

# class Itinerario:
#     def __init__(self, id, nome, default):
#         self.id = id
#         self.nome = nome
#         self.default = default

# class Luogo:
#     def __init__(self, id, nome, stato, latitudine, longitudine):
#         self.id = id
#         self.nome = nome
#         self.stato = stato
#         self.latitudine = latitudine
#         self.longitudine = longitudine






@appWebApi.route("/logout")
def closeAll():
    db.close()





if __name__ == "__main__":
    appWebApi.run(host='0.0.0.0', port=5000)











