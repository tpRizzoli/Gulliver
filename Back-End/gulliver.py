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
    def __init__(self, id, nome, luogo, difficolta, descrizione):
        self.id = id
        self.nome = nome
        self.luogo = luogo
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
             where l.nome = '%s'
             group by t.id;""" % (args.get('nomeLuogo'))
    
    
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        
        output = []

        for row in results:
            tipologia = Tipologia(row[0], row[1])
            output.append(tipologia.__dict__)

    except:
        print("Error: unable to fetch data")
        return 'Errore'

    return json.dumps(output, indent=4)


@app.route('/findAttivitaTipologie', methods=["GET"])
def findAttivitaTipologie():
    cursor = db.cursor()

    args = request.args

    nomeLuogo = args.get('nomeLuogo')
    idTipolgie = args.getlist('idTipologia')
    listaId = ', '.join(idTipolgie)
   
    sql= """SELECT a.id, a.nome, l.nome, a.difficolta, a.descrizione
            FROM attivita AS a
            JOIN tipologie AS t ON t.id = a.id_tipologia
            JOIN attivita_luoghi AS al ON al.id_attivita = a.id
            JOIN luoghi AS l ON l.id = al.id_luogo
            WHERE l.nome = '%s' AND t.id IN (%s);""" % (nomeLuogo, listaId)
   
    
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        
        output = []

        for row in results:
            utente = Attivita(row[0], row[1], row[2], row[3], row[4])
            output.append(utente.__dict__)
    except:
        print("Error: unable to fetch data")
        return 'Errore'

    return json.dumps(output, indent=4)


@app.route('/createItinerario', methods=['POST']) #mi serve un idItinerario

def createItinerario():

    args = request.args

    idUtente = int(args.get('idUtente'))

    try:
        idItinerario = int(args.get('idItinerario'))
    except:
        idItinerario = None

    try:
        nomeItinerario = args.get('nomeItinerario')
    except:
        nomeItinerario = None
    
    try:
        listaAttivita = args.getlist('idAttivita')
    except:
        listaAttivita = None

        
    cercaItinerarioNome = """SELECT * FROM itinerari WHERE nome = '%s';"""
    cercaItinerarioId = """SELECT * FROM itinerari WHERE id = %d;"""
    controllaRelazioneUtenteItinerario = """SELECT * FROM utenti_itinerari WHERE id_utente = %d AND id_itinerario = %d;"""

    creazioneItinerario = """INSERT INTO itinerari (nome) VALUES ('%s');"""
    creazioneRelazioniAttivitaItinerario = """INSERT INTO attivita_itinerari (id_attivita, id_itinerario) VALUES (%d, %d);"""
    creazioneRelazioneUtenteItinerario = """INSERT INTO utenti_itinerari (id_utente, id_itinerario) VALUES (%d, %d);"""

    if idItinerario != None and nomeItinerario != None:
        print('REQUEST_ERROR : Non posso ricevere sia idItinerario e nomeItinerario')
        return 'Errore'


    cursor = db.cursor() 
    

    if idItinerario != None: # controllo se l'itinerario è assegnato a questo utente
        try:
            cursor.execute(cercaItinerarioId % (idItinerario))
            i = cursor.fetchone()

            if i == None:
                print('REQUEST_ERROR : idItinerario inesistente')
                return 'Errore'

        except:
            print('QUERY_ERROR : Ricerca Itinerario per ID')
            return "Errore"

        try:
            cursor.execute(controllaRelazioneUtenteItinerario % (idUtente, idItinerario))
            r = cursor.fetchone()
        except:
            print('QUERY_ERROR : Controllo Relazione Relazioni Utente-Itinerario')
            return "Errore"

        if r == None: #non assegnato a questo utente
            try:
                cursor.execute(creazioneRelazioneUtenteItinerario % (idUtente, idItinerario))
                db.commit()
            except:
                print('QUERY_ERROR : Creazione Record Relazioni Utente-Itinerario')
                return "Errore"

            try:
                cursor.execute('SELECT * FROM itinerari WHERE id = %d;' % (idItinerario))
                i = Itinerario(*cursor.fetchone())
                output = i.__dict__
            except:
                print('QUERY_ERROR : Get Itinerario')
                return "Errore"
        else: # già assegnato a questo utente
            output = 'Itinerario gia assegnato ad utente'

    else: # cerco itinerari per nome
        try:
            cursor.execute(cercaItinerarioNome % (nomeItinerario))
            itinerariTrovati = cursor.fetchall()
        except:
            print('QUERY_ERROR : Ricerca Itinerari per Nome')
            return "Errore"

        if itinerariTrovati == (): # non esiste itinerario
            try:
                cursor.execute(creazioneItinerario % nomeItinerario)
                db.commit()
                
                cursor.execute('SELECT * FROM itinerari WHERE id = LAST_INSERT_ID()')
                itinerarioCreato = Itinerario(*cursor.fetchone())
            
            except:
                print('QUERY_ERROR : Creazione Record Itinerario')
                return "Errore"
            
            try:
                for val in listaAttivita:
                    cursor.execute(creazioneRelazioniAttivitaItinerario % (int(val), itinerarioCreato.id))
                db.commit()
            
            except:
                print('QUERY_ERROR : Creazione Record Relazioni Attività-Itinerario')
                return "Errore"

            try:
                cursor.execute(creazioneRelazioneUtenteItinerario % (idUtente, itinerarioCreato.id))
                db.commit()
            except:
                print('QUERY_ERROR : Creazione Record Relazioni Utente-Itinerario')
                return "Errore"
            
            output = itinerarioCreato.__dict__
                    
        else:
            output = 'Itinerario gia assegnato ad utente'
                
    
    
    return json.dumps(output, indent=4)

#lista degli itinerari che possiede un utente
@app.route('/findItinerariUtente',methods=['GET'])
def findItinerariUtente():
    cursor = db.cursor()

    args = request.args

    
    sql= 'SELECT i.* FROM itinerari i JOIN utenti_itinerari ui ON i.id = ui.id_itinerario WHERE ui.id_utente = %s;' % (int(args.get('idUtente')))
    
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        
        output = []
        for row in results:
            i = Itinerario(row[0], row[1], row[2])
            output.append(i.__dict__)
    except:
        print("Error: unable to fetch data")
        return 'Errore'

    return json.dumps(output, indent=4)

@app.route('/getDettagliItinerario', methods=['GET'])
def getDettagliItinerari():
    cursor = db.cursor()

    args = request.args

    idItinerario = int(args.get('idItinerario'))    
    
    sql = '''SELECT a.id, a.nome, a.descrizione, t.nome, a.difficolta
            FROM attivita a
            JOIN tipologie t ON a.id_tipologia = t.id
            JOIN attivita_itinerari ai ON a.id = ai.id_attivita
            WHERE ai.id_itinerario = %d;''' % (idItinerario)

    try:
        cursor.execute(sql)
        results = cursor.fetchall()

        output = []
        for row in results:
            output.append(Attivita(row[0], row[1], row[2], row[3], row[4]).__dict__)
            
    except:
        print('Error: unable to fetch data')
        return 'Errore'
    
    return json.dumps(output, indent=4)



@app.route('/createUser', methods=['POST'])
def createUser():
    cursor = db.cursor()
    args = request.args

    username = args.get("username")
    email = args.get("email")
    pwd = args.get("password")
    
    query = "INSERT INTO utenti (username, email, pwd) VALUES ('%s', '%s', '%s');"  % (username, email, pwd)

    try:
        cursor.execute(query)
        db.commit()

        try:
            cursor.execute('SELECT * FROM utenti WHERE id = LAST_INSERT_ID();')
            res = cursor.fetchone()
            output = Utente(res[0], res[1], res[2], res[3]).__dict__
        except:
            print('QUERY_ERROR : Get Utente appena registrato')
            return "Errore"

        return json.dumps(output, indent=4)
    
    except:
        print('Error: unable to fetch data')
        return 'Errore'
    
#login utente
@app.route('/getUser', methods=['GET'])
def getUser():
    cursor = db.cursor()

    args = request.args
    
    sql= "select * from utenti where username = '%s' and pwd = '%s';" % (args.get('utente'), args.get('password'))
    
    output = []

    try:
        cursor.execute(sql)
        res = cursor.fetchone()
        
        output = Utente(res[0], res[1], res[2], res[3]).__dict__
    except:
        print("Error: unable to fetch data")

    return json.dumps(output, indent=4)


#modifica del profilo utente
@app.route("/modificaProfilo/<id>", methods = ['PUT'])
def modificaProfilo(id):
    cursor = db.cursor()
    args = request.args

    username = args.get("username")
    email = args.get("email")
    password = args.get("password")

    sql= "UPDATE utenti SET username = '%s', email = '%s', pwd = '%s' WHERE id = %d" % (username, email, password, int(id))

    try:
        cursor.execute(sql)
        db.commit()

        output = Utente(id, username, email, password).__dict__

    except:
        print('Query error')
        return 'Errore'
        
    return json.dumps(output, indent=4)


# Elimina un itinerario   
@app.route('/eliminaItinerario', methods = ['DELETE'])
def deleteItinerario():
    cursor = db.cursor()
    args = request.args

    idItinerario = int(args.get('idItinerario'))
    idUtente = int(args.get('idUtente'))

    try:
        cursor.execute("DELETE FROM utenti_itinerari WHERE id_itinerario = %d AND id_utente = %d;" % (idItinerario, idUtente))

        cursor.execute("SELECT i.sysDefault FROM itinerari i WHERE id = %d;" % (idItinerario))
        itinerario = cursor.fetchone()

        if itinerario[0] == 0:        
            cursor.execute("DELETE FROM attivita_itinerari WHERE id_itinerario = %d;" % (idItinerario))
            cursor.execute("DELETE FROM itinerari WHERE id = %d;" % (idItinerario))

        db.commit()
    except:
        connection.rollback()
        print('Query Error')
        return 'Errore'

    return 'Itinerario eliminato'


# Ritorna elenco di Itinerari in base alla categoria scelta
@app.route("/findItinerariSuggeriti", methods=['GET'])
def findItinerariSuggeriti():
    
    nomeCategoria = request.args.get('categoria')
    cursor=db.cursor()  
    sql="""SELECT i.*
            FROM itinerari i 
            JOIN attivita_itinerari ai ON i.ID = ai.id_itinerario
            JOIN attivita_luoghi al ON ai.id_attivita = al.id_attivita
            JOIN luoghi l ON al.id_luogo = l.ID
            JOIN luoghi_categorie lc ON l.ID = lc.id_luogo
            JOIN categorie c ON lc.id_categoria = c.ID
            WHERE c.nome = '%s' AND i.sysDefault = 1
            GROUP BY i.id;""" % (nomeCategoria)
    try:
        cursor.execute(sql)
        result=cursor.fetchall()
            
        output=[]

        for row in result:
                output.append(Itinerario(row[0], row[1], row[2]).__dict__)
            
        return json.dumps(output, indent=4) 
                   
    except:
        return json.dumps({"message": "Error fetching itinerari"}, indent=4)
        
@app.route("/logout")
def closeAll():
    db.close()

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000)
