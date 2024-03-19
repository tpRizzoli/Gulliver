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





# Classi database
class Attivita:
    def __init__(self, id, nome, tipologia, difficolta, descrizione):
        self.id = id
        self.nome = nome
        self.tipologia = tipologia
        self.difficolta = difficolta
        self.descrizione = descrizione

class Utente:
    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

class Itinerario:
    def __init__(self, id, nome, default):
        self.id = id
        self.nome = nome
        self.default = default

class Luogo:
    def __init__(self, id, nome, stato, latitudine, longitudine):
        self.id = id
        self.nome = nome
        self.stato = stato
        self.latitudine = latitudine
        self.longitudine = longitudine

class Tipologia:
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome

class Categoria:
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome



# Trova le tipologie di attività in base al luogo indicato
@appWebApi.route('/findTipologie', methods=['GET'])
def fetchTipologieByLuogo():
    cursor = db.cursor()

    args = request.args

    sql = """select t.*
                from tipologie as t 
                join attivita as a on a.id_tipologia = t.id
                join attivita_luoghi as al on al.id_attivita = a.id
                join luoghi as l on l.id = al.id_luogo
                where l.nome = '""" + args.get('nomeLuogo') + """'
                group by t.id;""" 
    
    
    try:
        cursor.execute(sql)
        
        results = cursor.fetchall()
        output = []

        for row in results:
            tipolgia = Tipologia(row[0], row[1])
            output.append(tipologia)

    except:
        print("Error: unable to fetch data")

    return json.dumps(output, indent=4)





@appWebApi.route('/findItinerarioUtente',methods=['GET'])
def findItinerarioUtente():
    cursor = db.cursor()

    args = request.args

    
    sql= """SELECT u.id, u.username, i.id , i.nome 
            from utenti as u 
            join utenti_itinerari as ui on ui.id_utente = u.id 
            join itinerari as i on i.id = ui.id_itinerario 
            where i.nome='"""+ args.get('nomeItinerari') +"""';"""
    print(sql)
    
    try:
        cursor.execute(sql)
        
        results = []
        results = cursor.fetchall()


        for row in results:
            id_utente = row[0]
            utente = row[1]
            id_itinerario=row[2]
            itinerario = row[3]
            
            results.append(utente_itinerario( id_utente, utente, id_itinerario, itinerario))
    except:
        print("Error: unable to fetch data")
    return json.dumps(results, default=vars)




@appWebApi.route('/findAttivitaTipologie', methods=["GET"])
def findAttivitaTipologie():
    cursor = db.cursor()

    args = request.args

    idTipolgie = args.getlist('idTipologia')
    listaTipologie = ''
    
    for index, tip in enumerate(idTipolgie):
        if index == len(idTipolgie) - 1:
            listaTipologie += 't.id = ' + tip
        else:
            listaTipologie += 't.id = ' + tip + ' or '
    
    sql= """select a.*
            from attivita as a
            join tipologie as t on t.id = a.id_tipologia
            join attivita_luoghi as al on al.id_attivita = a.id
            join luoghi as l on l.id = al.id_luogo
            where l.id = """ + args.get('idLuogo') + """ and (""" + listaTipologie + """);"""
   
    
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        
        output = []

        for row in results:
            attivita = Attivita(row[0], row[1], row[2], row[3], row[4])
            output.append(attivita.__dict__)

    except:
        print("Error: unable to fetch data")

    return json.dumps(output, indent=4)

@appWebApi.route("/logout")
def closeAll():
    db.close()





if __name__ == "__main__":
    appWebApi.run(host='0.0.0.0', port=5000)











