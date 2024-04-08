import traceback
from flask import Flask, session, request, redirect, render_template 
from flask_session import Session
import pymysql


appWebApi = Flask(__name__)
# appWebApi.config["SESSION_PERMANENT"] = False
# appWebApi.config['SECRET_KEY'] = 'chiave_secreta'
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

#INIZIO GESTIONE ACCOUNT UTENTE -----------------------------------------------------------------------------------------------

#visualizzazione del profilo utente
@appWebApi.route("/profilo")
def getProfilo():
    if not session.get("id"):
        return redirect("/login")
    
    utente = session.get("id")
    cursor = db.cursor()
    sql = "SELECT username, email FROM utenti WHERE id ='%s';"
    #print(sql)

    try:
        cursor.execute(sql,(utente))
        results = cursor.fetchone()
        #print(results)
        username_utente = results[0]
        email_utente = results[1]
    except:
        print ("Error: cannot fetch data")
    
    query = "SELECT i.ID, i.nome , i.sysDefault\
        FROM utenti_itinerari ui\
        JOIN itinerari i ON ui.id_itinerario = i.ID\
        JOIN utenti u ON ui.id_utente = u.ID\
        WHERE u.username ='"+username_utente+"';"   #si potrebbe provare a usare l'id, ma al momento da errore
    
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
        sql = "SELECT ID FROM utenti WHERE username = %s AND pwd = %s"
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
            sql = "INSERT INTO utenti (username, email, pwd) VALUES (%s, %s, %s)"
            cursor.execute(sql, (username, email, pwd))
            db.commit()
            session['id'] = cursor.lastrowid

            return redirect('/profilo')
        except Exception:
            print("Errore durante la creazione dell'utente")
            traceback.print_exc()
            return render_template('registrazione.html', error='Registrazione fallita')
         
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
                sql= "update utenti set username = '%s', email = '%s', pwd = '%s' where id = '%s'" % (new_username, new_email, new_pwd, id_utente)
                cursor.execute(sql)
                db.commit()
                

                return redirect("/profilo")
        except:
            db.rollback()
            return render_template("Impossibile modificare l'utente")
    else:
        return redirect('/')

@appWebApi.route("/paginaModifica")
def paginaModifica():
    return render_template("modificaProfiloProva.html")
    
#logout utente chiusura della sessione dell'utente
@appWebApi.route("/logout")
def logout():
    session['id'] = None
    return redirect("/")

#FINE GESTIONE ACCOUNT UTENTE ------------------------------------------------------------------------------------------

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
            Where c.nome ='"+categoriaPassata+"'\
            GROUP BY i.nome;"
    
    # print(sql)
    
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            nome_itinerario = row[0]
            nome_categoria = row[1]
            listaItinerariXCategoria.append(Categoria(nome_itinerario, nome_categoria))
    except:
        print ("Error: cannot fetch data")
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
    
    # print(sql)
    listaTipologieXLuogo = []

    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            id_tipologia = row[0]
            nome_tipologia = row[1]
            listaTipologieXLuogo.append(Tipologia(id_tipologia, nome_tipologia))
    except:
        print ("Error: cannot fetch data")
    return render_template('sceltaTipologiaRES.html', destinazione = nomeLuogo, lista = listaTipologieXLuogo)


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
            print ("Error: cannot fetch data")

    return render_template('sceltaAttivitaRES.html', destinazione = nomeLuogo, lista = dizionarioAttivita)


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
            
    return render_template('sommarioRES.html', destinazione=nomeLuogo, sommario = sommarioAttivita)
    

@appWebApi.route("/SommarioDefault")
def getDefaultSummary():
    nomeItinerario = str(request.args.get('nomeItinerarioDef'))
    print(nomeItinerario)
    # i dati arrivano correttamente

    sql = "SELECT a.nome, a.difficolta, a.descrizione AS nome_attivita\
        FROM attivita_itinerari ai\
        JOIN itinerari i ON ai.id_itinerario = i.ID\
        JOIN attivita a ON ai.id_attivita = a.ID\
        WHERE i.nome = '"+nomeItinerario+"';"
    
    sommarioAttivita=[]
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

    except:
        print ("Error: cannot fetch data")
            

    return render_template("sommarioDefRES.html", nomeItinerario = nomeItinerario, lista = sommarioAttivita)



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
    print(idItinerario)
    idUtente = session.get("id")

    controlloPresenzaItinerario = "SELECT id, id_utente, id_itinerario \
                                    FROM utenti_itinerari \
                                    WHERE id_utente = %s AND id_itinerario = %s;"
    cursor.execute(controlloPresenzaItinerario, (idUtente, idItinerario))
    presenza = cursor.fetchone()
    print(presenza)

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
    print(nomeItinerario)

    cursor=db.cursor()
    ricercaIdItinerario = "SELECT id, sysDefault FROM itinerari WHERE nome = '"+nomeItinerario+"';"
    cursor.execute(ricercaIdItinerario)
    result = cursor.fetchone()
    if result: 
        idItinerario = result[0]
        sysDefault = result[1]
        print(idItinerario)
        print(sysDefault)
    else:
        return "Error: Itinerario non trovato"


    idUtente = session.get("id")

    if sysDefault == 1:
        try:
            eliminaItinerarioUtente = "DELETE FROM utenti_itinerari WHERE id_utente = %s AND id_itinerario = %s;"
            cursor.execute(eliminaItinerarioUtente, (idUtente, idItinerario))
            db.commit()
        except:
            return redirect("/profilo") ###!!!!!!!###
    else:
        try:
            eliminaItinerarioUtente = "DELETE FROM utenti_itinerari WHERE id_utente = %s AND id_itinerario = %s;"
            cursor.execute(eliminaItinerarioUtente, (idUtente, idItinerario))
            eliminaItinerario = "DELETE FROM itinerari WHERE id_itinerario = %s;"
            cursor.execute(eliminaItinerario,(idItinerario))
            db.commit()
        except:
            return redirect("/profilo") ###!!!!!!!###


    return redirect("/profilo")




@appWebApi.route("/ItinerarioSalvato", methods=["POST"])
def salvaItinerario():
    if not session.get("id"):
        return redirect("/login")

    listaAttivitaSommario = request.form.getlist('nomeAttivita')
    nuovoItinerario = request.form.get('nuovoItinerario')
    print("NOME ITINERARIO: ", nuovoItinerario)
    print("ATTIVITA SELEZIONATE:", listaAttivitaSommario)

    #recupero ID delle attività
    cursor = db.cursor()
    listaIDAttivita=[]
    for nomeAttivita in listaAttivitaSommario:
        # Esegui la query per ottenere l'ID dell'attività
        sql = "SELECT id FROM Attivita WHERE nome = %s"
        cursor.execute(sql,(nomeAttivita))
        result = cursor.fetchone()
        # print(result)
        if result:
            # Aggiungi l'ID alla lista
            listaIDAttivita.append(result[0])
        else:
            print("Errore: l'attività non esiste nel database.")
    print(listaIDAttivita)

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
        print ("Error: cannot fetch data")

    return redirect("/profilo")

#--------------------------------------------------------------------------------------------------------------------------------
# Classi database

# class Luogo:
#     def __init__(self, id, nome, stato, latitudine, longitudine):
#         self.id = id
#         self.nome = nome
#         self.stato = stato
#         self.latitudine = latitudine
#         self.longitudine = longitudine



# @appWebApi.route("/logout")
# def closeAll():
#     db.close()





if __name__ == "__main__":
    appWebApi.run(host='0.0.0.0', port=5000)

