import traceback
from flask import Flask, session, request, redirect, render_template, make_response
from flask_session import Session
import pymysql
import json


appWebApi = Flask(__name__)
appWebApi.config['SESSION_TYPE'] = 'filesystem'
Session(appWebApi)

# Configurazione connessione DB MySQL
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'password'
MYSQL_DB = 'gulliver'



# Connessione al DB
db = pymysql.connect(host = MYSQL_HOST, user = MYSQL_USER, password = MYSQL_PASSWORD, db = MYSQL_DB)

class Utente:
    id_utente = None
    username_utente = None
    email_utente = None
    password_utente = None
    def __init__(self, id, username, email, password):
        self.id_utente = id
        self.username_utente = username
        self.email_utente = email
        self.password_utente = password

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

class Attivita:
    nome_attivita = None
    difficolta = None
    descrizione_attivita = None
    def __init__(self, nome, difficolta, descrizione):
        self.nome_attivita = nome
        self.difficolta = difficolta
        self.descrizione_attivita = descrizione

class Itinerario:
    id_itinerario = None
    nome_itinerario = None
    default_itinerario = None
    def __init__(self, id, nome, default):
        self.id_itinerario = id
        self.nome_itinerario = nome
        self.default_itinerario = default

class Luogo:
    id_luogo = None
    nome_luogo = None
    stato_luogo = None
    latitudine_luogo = None
    longitudine_luogo = None
    def __init__(self, id, nome, stato, latitudine, longitudine):
        self.id_luogo = id
        self.nome_luogo = nome
        self.stato_luogo = stato
        self.latitudine_luogo = latitudine
        self.longitudine_luogo = longitudine




#visualizzazione del profilo utente
@appWebApi.route("/profilo")
def getProfilo():
    if not session.get("id"):
        return redirect("/login")
    
    utente = session.get("id")
    cursor = db.cursor()
    sql = "SELECT username, email FROM utenti WHERE id ='%s';"

    try:
        cursor.execute(sql,(utente))
        results = cursor.fetchone()
        username_utente = results[0]
        email_utente = results[1]
    except:
        print ("Error: cannot fetch data")
    
    query = "SELECT i.ID, i.nome , i.sysDefault\
        FROM utenti_itinerari ui\
        JOIN itinerari i ON ui.id_itinerario = i.ID\
        JOIN utenti u ON ui.id_utente = u.ID\
        WHERE u.username ='"+username_utente+"';"
    
    listaItinerariUtenti = []
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            id_itinerario = row[0]
            nome_itinerario = row[1]
            default_itinerario = row[2]
            listaItinerariUtenti.append(Itinerario(id_itinerario, nome_itinerario, default_itinerario))
    except:
        print ("Error: cannot fetch data")

    
    return render_template("profiloRES.html", user = username_utente, email = email_utente, lista = listaItinerariUtenti)

#login utente e creazione della sessione utente
@appWebApi.route("/login", methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Query per verificare le credenziali nel database
        sql = "SELECT ID FROM utenti WHERE username = %s AND BINARY pwd = %s"
        cursor = db.cursor()
        cursor.execute(sql, (username, password))
        user = cursor.fetchone()

        if user:
            session['id'] = user[0]
            return redirect('/profilo')
        else:
            print("Errore: credenziali errate")
            return render_template('loginPage.html')
    return render_template('loginPage.html')

#registrazione utente e creazione della sessione utente
@appWebApi.route('/registrazione', methods=['POST','GET'])
def registrazione():
    if request.method == 'POST': 

        cursor = db.cursor()
        username = request.form['username']
        email = request.form['email']
        pwd = request.form['password']

        try:
            sql = "INSERT INTO utenti (username, email, pwd) VALUES (%s, %s, %s);"
            cursor.execute(sql, (username, email, pwd))
            db.commit()
            session['id'] = cursor.lastrowid

            return redirect('/profilo')
        except:
            print("Errore durante la creazione dell'utente")
            
         
    else:
        return render_template('registrazione.html')

#modifica del profilo utente
@appWebApi.route("/modificaProfilo", methods = ['PUT', 'POST'])
def modificaProfilo():
    if request.method == 'POST':
        try:
            id_utente = session['id']
            new_username = request.form["username"]
            new_email = request.form["email"]
            new_pwd = request.form["password"]

            with db.cursor() as cursor:
                sql= "update utenti set username ='%s', email =REPLACE(TRIM(BOTH ' ' FROM '%s'), ' ', ''), pwd = '%s' where id = '%s'; " % (new_username, new_email, new_pwd, id_utente)
                cursor.execute(sql)
                db.commit()
                
                return redirect("/profilo")
        except:
            db.rollback()
            print("Errore: Username o email già esistenti")
            return redirect("/paginaModifica")
    else:
        return redirect('/')

@appWebApi.route("/paginaModifica")
def paginaModifica():
    return render_template("modificaProfilo.html")
    
#logout utente chiusura della sessione dell'utente
@appWebApi.route("/logout")
def logout():
    session['id'] = None
    return redirect("/")

#homepage
@appWebApi.route("/")
def main():
    return render_template('homepage.html')

@appWebApi.route("/idee")
def getCategorie():
    categoriaPassata = request.args.get('categoria')

    listaItinerariXCategoria = []
    cursor = db.cursor()
    sql = "SELECT i.nome AS nome_itinerario, c.nome AS nome_categoria \
            FROM itinerari i \
            JOIN attivita_itinerari ai ON i.ID = ai.id_itinerario\
            JOIN attivita_luoghi al ON ai.id_attivita = al.id_attivita\
            JOIN luoghi l ON al.id_luogo = l.ID\
            JOIN luoghi_categorie lc ON l.ID = lc.id_luogo\
            JOIN categorie c ON lc.id_categoria = c.ID\
            Where c.nome ='"+categoriaPassata+"' AND i.sysDefault = 1\
            GROUP BY i.nome;"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            nome_itinerario = row[0]
            nome_categoria = row[1]
            listaItinerariXCategoria.append(Categoria(nome_itinerario, nome_categoria))
    except:
        print ("Errore nel recupero dei dati")
    return render_template('ideeRES.html',  categoria = categoriaPassata, lista = listaItinerariXCategoria)

@appWebApi.route("/destinazione") 
def getTipologieAttivita():
    nomeLuogo = str(request.args.get('destinazione'))

    cursor = db.cursor()
    sql = "SELECT t.ID AS id_tipologia, t.nome AS nome_tipologia\
        FROM luoghi l\
        JOIN attivita_luoghi al ON l.ID = al.id_luogo\
        JOIN attivita a ON al.id_attivita = a.ID\
        JOIN tipologie t ON a.id_tipologia = t.ID\
        WHERE l.nome ='"+nomeLuogo+"'\
        GROUP BY t.id;"
    
    listaTipologieXLuogo = []
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            id_tipologia = row[0]
            nome_tipologia = row[1]
            listaTipologieXLuogo.append(Tipologia(id_tipologia, nome_tipologia))
    except:
        print ("Errore nel recupero dei dati")

    luogo1=[]    
    try:
        slq2 = "SELECT * FROM luoghi WHERE nome = %s"
        cursor.execute(slq2,(nomeLuogo))
        results2 = cursor.fetchall()
        for row in results2:
            id_luogo = row[0]
            nome_luogo = row[1]
            stato_luogo = row[2]
            latitudine_luogo = row[3]
            longitudine_luogo = row[4]
            luogo1.append(Luogo(id_luogo, nome_luogo, stato_luogo, latitudine_luogo, longitudine_luogo))
    except:
        print ("Errore nel recupero dei dati")       

    return render_template('sceltaTipologiaRES.html', destinazione = nomeLuogo, lista = listaTipologieXLuogo, luogo = luogo1)

@appWebApi.route("/Attivita", methods=["POST"]) 
def getAttivita():
    nomeLuogo = request.form.get('destinazione')
    listaTipologieSelezionate = request.form.getlist('opzioneDinamica')
    print("Destinazione: ", nomeLuogo)
    print("Tipologie selezionate:", listaTipologieSelezionate)
    
    dizionarioAttivita = {}
    cursor = db.cursor()
    
    for i in range(len(listaTipologieSelezionate)): 
        sql = "SELECT a.nome, a.difficolta, a.descrizione FROM attivita as a\
            JOIN tipologie t ON a.id_tipologia = t.ID\
            JOIN attivita_luoghi al ON a.ID = al.id_attivita\
            JOIN luoghi l ON al.id_luogo = l.ID\
            WHERE l.nome = '"+nomeLuogo+"' " + "AND t.nome " "IN "+"('"+(listaTipologieSelezionate[i])+"');"

        dizionarioAttivita[listaTipologieSelezionate[i]] = []

        print(sql)
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            print(results)
            for row in results:
                nome_attivita = row[0]
                difficolta = row[1]
                descrizione_attivita = row[2]
                dizionarioAttivita[listaTipologieSelezionate[i]].append(Attivita(nome_attivita, difficolta, descrizione_attivita))

        except:
            print ("Errore nel recupero dei dati")
    
    luogo1=[]    
    try:
        slq2 = "SELECT * FROM luoghi WHERE nome = %s"
        cursor.execute(slq2,(nomeLuogo))
        results2 = cursor.fetchall()
        for row in results2:
            id_luogo = row[0]
            nome_luogo = row[1]
            stato_luogo = row[2]
            latitudine_luogo = row[3]
            longitudine_luogo = row[4]
            luogo1.append(Luogo(id_luogo, nome_luogo, stato_luogo, latitudine_luogo, longitudine_luogo))
    except:
        print ("Errore nel recupero dei dati") 
            
    return render_template('sceltaAttivitaRES.html', destinazione = nomeLuogo, lista = dizionarioAttivita, luogo = luogo1)

@appWebApi.route("/Sommario", methods=['POST'])
def createSommario():
    nomeLuogo = request.form.get('destinazione')
    listaAttivitaSelezionate = request.form.getlist('opzioneDinamica')
    print("Destinazione: ", nomeLuogo)
    print("Tipologie selezionate:", listaAttivitaSelezionate)

    sommarioAttivita=[]
    cursor=db.cursor()

    for i in range(len(listaAttivitaSelezionate)):
        sql = "SELECT a.nome, a.difficolta, a.descrizione FROM attivita as a\
            JOIN attivita_luoghi al ON a.ID = al.id_attivita\
            JOIN luoghi l ON al.id_luogo = l.ID\
            WHERE a.nome = '"+(listaAttivitaSelezionate[i])+"'\
            AND l.nome = '"+nomeLuogo+"';"
        
        print(sql)
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            print(results)
            for row in results:
                nome_attivita = row[0]
                difficolta = row[1]
                descrizione_attivita = row[2]
                sommarioAttivita.append(Attivita(nome_attivita, difficolta, descrizione_attivita))

        except:
            print ("Error: cannot fetch data")

    luogo1=[]    
    try:
        slq2 = "SELECT * FROM luoghi WHERE nome = %s"
        cursor.execute(slq2,(nomeLuogo))
        results2 = cursor.fetchall()
        for row in results2:
            id_luogo = row[0]
            nome_luogo = row[1]
            stato_luogo = row[2]
            latitudine_luogo = row[3]
            longitudine_luogo = row[4]
            luogo1.append(Luogo(id_luogo, nome_luogo, stato_luogo, latitudine_luogo, longitudine_luogo))
    except:
        print ("Error: cannot fetch data")  
            
    return render_template('sommarioRES.html', destinazione=nomeLuogo, sommario = sommarioAttivita, luogo = luogo1)       
    
@appWebApi.route("/SommarioDefault")
def getDefaultSummary():
    nomeItinerario = str(request.args.get('nomeItinerarioDef'))
    print(nomeItinerario)

    sql = "SELECT a.nome, a.difficolta, a.descrizione AS nome_attivita\
        FROM attivita_itinerari ai\
        JOIN itinerari i ON ai.id_itinerario = i.ID\
        JOIN attivita a ON ai.id_attivita = a.ID\
        WHERE i.nome = '"+nomeItinerario+"';"
    
    sommarioAttivita=[]
    listaNomeAttivita=[]
    cursor=db.cursor()

    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        print(results)
        for row in results:
            nome_attivita = row[0]
            difficolta = row[1]
            descrizione_attivita = row[2]
            sommarioAttivita.append(Attivita(nome_attivita, difficolta, descrizione_attivita))
            listaNomeAttivita.append(nome_attivita)
            
    except:
        print ("Errore nel recupero dei dati")

    print('lista nome attivita: ', listaNomeAttivita)
    
    strListaAttività = ""
    for i in range(len(listaNomeAttivita)):
        strListaAttività += "'"  + listaNomeAttivita[i] + "'"
        if i < len(listaNomeAttivita) - 1:
            strListaAttività += ", "

    cercaLuogo = "SELECT l.nome AS nome_luogo\
        FROM luoghi l\
        JOIN attivita_luoghi al ON l.ID = al.id_luogo\
        JOIN attivita a ON al.id_attivita = a.ID\
        WHERE a.nome IN ("+strListaAttività+");"
    
    try:
        cursor.execute(cercaLuogo)
        result = cursor.fetchone()
        nomeLuogo = result[0]
        print(nomeLuogo)
    except:
        print ("Errore nel recupero dei dati")

    luogo1=[]    
    try:
        slq2 = "SELECT * FROM luoghi WHERE nome = %s"
        cursor.execute(slq2,(nomeLuogo))
        results2 = cursor.fetchall()
        for row in results2:
            id_luogo = row[0]
            nome_luogo = row[1]
            stato_luogo = row[2]
            latitudine_luogo = row[3]
            longitudine_luogo = row[4]
            luogo1.append(Luogo(id_luogo, nome_luogo, stato_luogo, latitudine_luogo, longitudine_luogo))
    except:
        print ("Errore nel recupero dei dati")      

    return render_template("sommarioDefRES.html", nomeItinerario = nomeItinerario, lista = sommarioAttivita, luogo = luogo1)

@appWebApi.route("/SalvaDefault", methods=["POST"])
def salvaDefault():
    if not session.get("id"):
        return redirect("/login")
    
    nomeItinerario = request.form.get('nomeItinerario')
    print(nomeItinerario)

    cursor=db.cursor()
    ricercaIdItinerario = "SELECT ID FROM itinerari WHERE nome = '"+nomeItinerario+"';"
    cursor.execute(ricercaIdItinerario)
    idItinerario = cursor.fetchone()
    idUtente = session.get("id")

    controlloPresenzaItinerario = "SELECT id, id_utente, id_itinerario \
                                    FROM utenti_itinerari \
                                    WHERE id_utente = %s AND id_itinerario = %s;"
    cursor.execute(controlloPresenzaItinerario, (idUtente, idItinerario))
    presenza = cursor.fetchone()

    if presenza == None:
        addItinerario = "INSERT INTO utenti_itinerari (id_utente, id_itinerario)\
            SELECT u.ID, i.ID\
            FROM utenti u, itinerari i\
            WHERE u.id = %s\
            AND i.id = %s;"

        cursor.execute(addItinerario, (idUtente, idItinerario))
        db.commit()

    return redirect("/profilo")
    
@appWebApi.route("/DeleteItinerarioUtente")
def deleteItinerarioUtente():
    nomeItinerario = str(request.args.get('nomeItinerarioDelete'))

    cursor=db.cursor()
    ricercaIdItinerario = "SELECT id, sysDefault FROM itinerari WHERE nome = '"+nomeItinerario+"';"
    cursor.execute(ricercaIdItinerario)
    result = cursor.fetchone()
    if result: 
        idItinerario = result[0]
        sysDefault = result[1]
    else:
        return "Error: Itinerario non trovato"

    idUtente = session.get("id")

    if sysDefault == 1:
        try:
            eliminaItinerarioUtente = "DELETE FROM utenti_itinerari WHERE id_utente = %s AND id_itinerario = %s;"
            cursor.execute(eliminaItinerarioUtente, (idUtente, idItinerario))
            db.commit()
        except:
            print ("Errore nel recupero dei dati")
    else:
        try:
            eliminaItinerarioUtente = "DELETE FROM utenti_itinerari WHERE id_utente = %s AND id_itinerario = %s;"
            cursor.execute(eliminaItinerarioUtente, (idUtente, idItinerario))
            eliminaAttivitaItinerario = "DELETE FROM attivita_itinerari WHERE id_itinerario = %s;"
            cursor.execute(eliminaAttivitaItinerario,(idItinerario))
            eliminaItinerario = "DELETE FROM itinerari WHERE id = %s;"
            cursor.execute(eliminaItinerario,(idItinerario))
            db.commit()
        except:
            print ("Errore nel recupero dei dati")

    return redirect("/profilo")

@appWebApi.route("/ItinerarioSalvato", methods=["POST"])
def salvaItinerario():
    if not session.get("id"):
        return redirect("/login")

    listaAttivitaSommario = request.form.getlist('nomeAttivita')
    nuovoItinerario = request.form.get('nuovoItinerario')

    cursor = db.cursor()
    listaIDAttivita=[]
    for nomeAttivita in listaAttivitaSommario:
        sql = "SELECT id FROM Attivita WHERE nome = %s"
        cursor.execute(sql,(nomeAttivita))
        result = cursor.fetchone()
        if result:
            listaIDAttivita.append(result[0])
        else:
            print("Errore: l'attività non esiste nel database.")

    try:
        creazioneItinerario = "INSERT INTO itinerari (nome) VALUES ('"+nuovoItinerario+"');"
        cursor.execute(creazioneItinerario)
        db.commit()

        cursor.execute("SELECT MAX(id) FROM itinerari;")
        last_insert_id = cursor.fetchone()[0]
        db.commit()
        print("Ultimo ID_itinerario:", last_insert_id)

        for i in range(len(listaIDAttivita)):
            creazioneRelazioniAttivitaItinerario = "INSERT INTO attivita_itinerari (id_attivita, id_itinerario)\
                VALUES ("+str(listaIDAttivita[i])+", "+str(last_insert_id)+");"
            cursor.execute(creazioneRelazioniAttivitaItinerario)
            db.commit()

        idUtente = session.get("id")
        creazioneRelazioneUtenteItinerario = "INSERT INTO utenti_itinerari (id_utente, id_itinerario)\
                 VALUES ("+str(idUtente)+", "+str(last_insert_id)+");"
        cursor.execute(creazioneRelazioneUtenteItinerario)
        db.commit()

    except:
        print ("Errore nel recupero dei dati")

    return redirect("/profilo")


# !!!!------------------------ API ANDROID ------------------------!!!!!

# Classi database
class Attivita_API:
    def __init__(self, id, nome, luogo, difficolta, descrizione):
        self.id = id
        self.nome = nome
        self.luogo = luogo
        self.difficolta = difficolta
        self.descrizione = descrizione

class Utente_API:
    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

class Itinerario_API:
    def __init__(self, id, nome, default):
        self.id = id
        self.nome = nome
        self.default = default

class Luogo_API:
    def __init__(self, id, nome, stato, latitudine, longitudine):
        self.id = id
        self.nome = nome
        self.stato = stato
        self.latitudine = latitudine
        self.longitudine = longitudine

class Tipologia_API:
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome

class Categoria_API:
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome

# Trova le tipologie di attività in base al luogo indicato
@appWebApi.route('/api/findTipologie', methods=['GET'])
def fetchTipologieByLuogoAPI():
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
            tipologia = Tipologia_API(row[0], row[1])
            output.append(tipologia.__dict__)

    except:
        print("Error: unable to fetch data")
        return 'Errore'

    return json.dumps(output, indent=4)


@appWebApi.route('/api/findAttivitaTipologie', methods=["GET"])
def findAttivitaTipologieAPI():
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
            utente = Attivita_API(row[0], row[1], row[2], row[3], row[4])
            output.append(utente.__dict__)
    except:
        print("Error: unable to fetch data")
        return 'Errore'

    return json.dumps(output, indent=4)


@appWebApi.route('/api/createItinerario', methods=['POST']) #mi serve un idItinerario
def createItinerarioAPI():

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
                i = Itinerario_API(*cursor.fetchone())
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
                itinerarioCreato = Itinerario_API(*cursor.fetchone())
            
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
@appWebApi.route('/api/findItinerariUtente',methods=['GET'])
def findItinerariUtenteAPI():
    cursor = db.cursor()

    args = request.args

    
    sql= 'SELECT i.* FROM itinerari i JOIN utenti_itinerari ui ON i.id = ui.id_itinerario WHERE ui.id_utente = %d;' % (int(args.get('idUtente')))
    
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        
        output = []
        for row in results:
            i = Itinerario_API(row[0], row[1], row[2])
            output.append(i.__dict__)
    except:
        print("Error: unable to fetch data")
        return 'Errore'

    return json.dumps(output, indent=4)

@appWebApi.route('/api/getDettagliItinerario', methods=['GET'])
def getDettagliItinerariAPI():
    cursor = db.cursor()

    args = request.args

    idItinerario = int(args.get('idItinerario'))    
    
    sql = '''SELECT a.id, a.nome, a.descrizione, a.difficolta, l.id, l.nome, l.stato, l.longitudine, l.latitudine
            FROM attivita a
            JOIN attivita_luoghi al ON a.id = al.id_attivita
            JOIN luoghi l ON l.id = al.id_luogo
            JOIN attivita_itinerari ai ON a.id = ai.id_attivita
            WHERE ai.id_itinerario = %d;''' % (idItinerario)

    try:
        cursor.execute(sql)
        results = cursor.fetchall()

        output = []
        for row in results:
            d = {
                'idAttivita' : row[0],
                'nomeAttivita' : row[1],
                'descrizioneAttivita' : row[2],
                'difficoltaAttivita' : row[3],
                'idLuogo' : row[4],
                'nomeLuogo' : row[5],
                'statoLuogo' : row[6],
                'latitudine' : row[7],
                'longitudine' : row[8]
            }
            output.append(d)
            
    except:
        print('Error: unable to fetch data')
        return 'Errore'
    
    return json.dumps(output, indent=4)


@appWebApi.route('/api/getDettagliAttivita', methods=['GET'])
def getDettagliAttivitaAPI():
    cursor = db.cursor()

    args = request.args

    idAttivita = args.getlist('idAttivita')
    listaId = ', '.join(idAttivita)    
    
    sql = '''SELECT a.id, a.nome, a.descrizione, a.difficolta, l.id, l.nome, l.stato, l.longitudine, l.latitudine
            FROM attivita a
            JOIN attivita_luoghi al ON a.id = al.id_attivita
            JOIN luoghi l ON l.id = al.id_luogo
            WHERE a.id IN (%s);''' % (listaId)

    try:
        cursor.execute(sql)
        response = cursor.fetchall()

        output = []

        for row in response:
            d = {
                    'idAttivita' : row[0],
                    'nomeAttivita' : row[1],
                    'descrizioneAttivita' : row[2],
                    'difficoltaAttivita' : row[3],
                    'idLuogo' : row[4],
                    'nomeLuogo' : row[5],
                    'statoLuogo' : row[6],
                    'latitudine' : row[7],
                    'longitudine' : row[8]
                }
            output.append(d)
        
    except:
        print('Error: unable to fetch data')
        return 'Errore'
    
    return json.dumps(output, indent=4)



@appWebApi.route('/api/createUser', methods=['POST'])
def createUserAPI():
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
            output = Utente_API(res[0], res[1], res[2], res[3]).__dict__
        except:
            print('QUERY_ERROR : Get Utente appena registrato')
            return "Errore"

        return json.dumps(output, indent=4)
    
    except:
        print('Error: unable to fetch data')
        return 'Errore'
    
#login utente
@appWebApi.route('/api/getUser', methods=['GET'])
def getUserAPI():
    cursor = db.cursor()

    args = request.args
    
    sql= "select * from utenti where username = '%s' and pwd = '%s';" % (args.get('utente'), args.get('password'))
    
    output = []

    try:
        cursor.execute(sql)
        res = cursor.fetchone()
        
        if res != None:
            output = Utente_API(res[0], res[1], res[2], res[3]).__dict__
        else:
            output = None
    except:
        print("Error: unable to fetch data")

    return json.dumps(output, indent=4)


#modifica del profilo utente
@appWebApi.route("/api/modificaProfilo/<id>", methods = ['PUT'])
def modificaProfiloAPI(id):
    cursor = db.cursor()
    args = request.args

    username = args.get("username")
    email = args.get("email")
    password = args.get("password")

    sql= "UPDATE utenti SET username = '%s', email = '%s', pwd = '%s' WHERE id = %d" % (username, email, password, int(id))

    try:
        cursor.execute(sql)
        db.commit()

        output = Utente_API(id, username, email, password).__dict__

    except:
        print('Query error')
        return 'Errore'
        
    return json.dumps(output, indent=4)


# Elimina un itinerario   
@appWebApi.route('/api/eliminaItinerario', methods = ['DELETE'])
def deleteItinerarioAPI():
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
        db.rollback()
        print('Query Error')
        return 'Errore'

    return 'Itinerario eliminato!'


# Ritorna elenco di Itinerari in base alla categoria scelta
@appWebApi.route("/api/findItinerariSuggeriti", methods=['GET'])
def findItinerariSuggeritiAPI():
    
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
                output.append(Itinerario_API(row[0], row[1], row[2]).__dict__)
            
        return json.dumps(output, indent=4) 
                   
    except:
        return json.dumps({"message": "Error fetching itinerari"}, indent=4)

if __name__ == "__main__":
    appWebApi.run(host='0.0.0.0', port=5000)

