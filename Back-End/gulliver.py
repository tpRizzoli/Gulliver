# Gulliver Back-End

from flask import Flask, render_template, request
import pymysql
import json
import jsonify

app = Flask(__name__)

# Configurazione connessione DB MySQL
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'password'
MYSQL_DB = 'gulliver'



# Connessione al DB
db = pymysql.connect(host = MYSQL_HOST, user = MYSQL_USER, password = MYSQL_PASSWORD, db = MYSQL_DB)


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
@app.route('/findTipologie', methods=['GET'])
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



@app.route('/getUser', methods=['GET'])
def getUser():
    cursor = db.cursor()

    args = request.args

    
    sql= """select * from utenti where username = '""" + args.get('utente') + """' and pwd = '""" + args.get('password') + """';"""
    
    
    try:
        cursor.execute(sql)
        
        output = []
        results = cursor.fetchall()


        for row in results:
            utente = Utente(row[0], row[1], row[2], row[3])
            output.append(utente)
    except:
        print("Error: unable to fetch data")
    return json.dumps(output, indent=4)



#@app.route('/findItinerarioUtente',methods=['GET'])
#def findItinerarioUtente():
#    cursor = db.cursor()

#    args = request.args

    
#    sql= """select * from utenti where username = '""" + args.get('utente') + """' and pwd = '""" + args.get('password') + """';"""
#    print(sql)
    
#    try:
#        cursor.execute(sql)
        
#        results = []
#        results = cursor.fetchall()


#        for row in results:
#            id = row[0]
#            username = row[1]
#            password = row [2]
#            results.append(Utente(id, username, password))
#    except:
#        print("Error: unable to fetch data")
#    return json.dumps(results, default=vars)


@app.route('/findAttivitaTipologie', methods=["GET"])
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

@app.route("/logout")
def closeAll():
    db.close()

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000)
