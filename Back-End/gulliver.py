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


# Restituisce una lista di Attività in base al Luogo e alle Tipologie indicate 
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









# Crea un nuovo Itinerario nel Database
@app.route('/createItinerario', methods=['POST']) #mi serve un idItinerario
def createItinerario():
    cursor = db.cursor()

    args = request.args

    output = []

    controllaItinerario = """SELECT * FROM itinerari WHERE nome = '%s';"""
    controllaRelazioneUtenteItinerario = """SELECT * FROM utenti_itinerari WHERE id_itinerario = %d AND id_utente = %d;"""

    creazioneItinerario = """INSERT INTO itinerari (nome) VALUES ('%s');"""
    creazioneRelazioneUtenteItinerario = """INSERT INTO utenti_itinerari (id_utente, id_itinerario) VALUES (%d, %d);"""
    creazioneRelazioniAttivitaItinerario = """INSERT INTO attivita_itinerari (id_attivita, id_itinerario) VALUES (%d, %d)"""

    idUtente = int(args.get('idUtente'))
    nomeItinerario = args.get('nomeItinerario')
    listaAttivita = args.getlist('idAttivita')

    idItinerario = None
    
    try: 
        cursor.execute(controllaItinerario % (nomeItinerario)) #controllo se esiste un itinerario con questo nome
        db.commit()
        itinerari = cursor.fetchall()

        if itinerari != (): # se esiste almeno un itinerario con quel nome, controllo se uno ha una relazione con l'utente
            relazioneTrovata = False
            for itinerario in itinerari:
               
                try:
                    cursor.execute(controllaRelazioneUtenteItinerario % (itinerario[0], idUtente)) #controllo se quell'itinerario è già assegnato a qualcuno
                    relazione = cursor.fetchone()

                    if relazione != None: 
                        relazioneTrovata = True
                        break
                    
                except:
                    print('!!! Query fallita: controllo Relazione Utenti-Itinerario !!!')
                
            if relazioneTrovata == True: #se c'è relazione, lo comunico e termino
                output.append("Itinerario già presente per questo utente")
                return json.dumps(output, indent=4)

            else: #se non c'è relazione, associo l'utente all'itinerario e aggiungo le attivita
                print(creazioneRelazioneUtenteItinerario % (idUtente, idItinerario))
                try:
                    cursor.execute(creazioneRelazioneUtenteItinerario % (idUtente, idItinerario)) # crea record tabella Utente-Itinerario
                    db.commit()
                except:
                    print('!!! Query fallita: creazione relazione Utente-Itinerario !!!')

                queryAttivita = ''
                    
                for index, att in enumerate(listaAttivita):
                    if index == len(listaAttivita) - 1:
                        queryAttivita += att
                    else:
                        queryAttivita += att + ', '

                try:
                    cursor.execute(creazioneRelazioniAttivitaItinerario % (queryAttivita, relazione[3]))
                except:
                    print('!!! Query fallita: creazione relazione Attivita-Itinerario !!!')

                for row in results: #sostituire ROW con qualcosa
                    output.append(Itinerario(row[0], row[1], row[2]).__dict__)
                    return json.dumps(output, indent=4)
        else: 
            try:
                cursor.execute(creazioneItinerario % (nomeItinerario)) # crea nuovo itinerario e tabella di relazione
                db.commit()
            except:
                print('!!! Query fallita: createItinerario!!!')

            try:    
                cursor.execute("SELECT LAST_INSERT_ID()") #reupera id itinerario creato
                db.commit()
                idItinerarioCreato = cursor.fetchone()[0]
            except:
                print('!!! Query fallita: idItinerarioCreato!!!')

            try:
                cursor.execute(creazioneTabellaRelazioneUtenteItinerario % (idUtente, idItinerarioCreato)) # crea record tabella Utente-Itinerario
            except:
                print('!!! Query fallita: creazioneTabellaUtenteItinerario!!!')

            queryAttivita = ''
                    
            for index, att in enumerate(listaAttivita):
                if index == len(listaAttivita) - 1:
                    queryAttivita += att
                else:
                    queryAttivita += att + ', '

            try:
                cursor.execute(creazioneTabellaRelazioneAttivitaItinerario % (queryAttivita, idItinerarioCreato))
            except:
                print('!!! Query fallita: creazioneTabellaAttivitaItinerario!!!')


            for row in results:
                output.append(Itinerario(row[0], row[1], row[2]).__dict__)
                return json.dumps(output, indent=4)
    except:
        print("!!! Query fallita: controllaItinerari !!!")

    return json.dumps("Qualcosa non va!", indent=4)













# Restituisce la lista di Itinerari salvati dall'utente
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
        
        results = cursor.fetchall()

        output = []

        for row in results:
            dictionary = {
                'id_utente': row[0],
                'utente': row[1],
                'id_itinerario': row[2],
                'itinerario': row[3]
            }
            
            
            output.append(dictionary)
    except:
        print("Error: unable to fetch data")
    return json.dumps(output, indent=4)

# Restituisce i dati di un utente (Login)
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
            output.append(utente.__dict__)
    except:
        print("Error: unable to fetch data")
    return json.dumps(output, indent=4)

@app.route("/logout")
def closeAll():
    db.close()

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000)
