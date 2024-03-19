# Gulliver Back-End

from flask import Flask, render_template, request
import pymysql
import json

app = Flask(__name__)

# Configurazione connessione DB MySQL
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'ciao'
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
    print(sql)
    
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
    print(sql)
    
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


@app.route('/findItinerarioUtente',methods=['GET'])
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



@app.route("/logout")
def closeAll():
    db.close()

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000)
