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



"""Trova le tipologie di attività in base al luogo indicato"""
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
        
        results = []
        results = cursor.fetchall()

        for row in results:
            id = row[0]
            nome = row[1]
            results.append(Tipologia(id, nome))

    except:
        print("Error: unable to fetch data")

    return json.dumps(results, default=vars)



@app.route('/getUser', methods=['GET'])
def getUser():
    cursor = db.cursor()

    args = request.args

    
    sql= """select * from utenti where username = '""" + args.get('utente') + """' and pwd = '""" + args.get('password') + """';"""
    
    
    try:
        cursor.execute(sql)
        
        results = []
        results = cursor.fetchall()


        for row in results:
            id = row[0]
            username = row[1]
            password = row [2]
            results.append(Utente(id, username, password))
    except:
        print("Error: unable to fetch data")
    return json.dumps(results, default=vars)



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
    print(sql)
   
    
    try:
        cursor.execute(sql)
        
        results = []
        results = cursor.fetchall()


        for row in results:
            id = row[0]
            nome = row[1]
            tipologia = row [2]
            difficolta = row [3]
            descrizione = row [4]
            results.append(Attivita(id, nome, tipologia, difficolta, descrizione))

    except:
        print("Error: unable to fetch data")

    return json.dumps(results, default=vars)

@app.route("/logout")
def closeAll():
    db.close()

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000)
