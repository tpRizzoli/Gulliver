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

@appWebApi.route("/prova")
def prova():
    return render_template("provacss.html")

@appWebApi.route("/profilo")
def getProfilo():
    if not session.get("username"):
        return redirect("/login")
    
    utente = session.get("username")
    cursor = db.cursor()
    sql = "SELECT username, email FROM utenti WHERE username ='"+utente+"';"
    #print(sql)

    try:
        cursor.execute(sql)
        results = cursor.fetchone()
        #print(results)
        username_utente = results[0]
        email_utente = results[1]
    except:
        print ("Error: cannot fetch data")
    
    return render_template("profiloRES.html", user = username_utente, email = email_utente)

    
@appWebApi.route("/login", methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Query per verificare le credenziali nel database
        sql = "SELECT username FROM utenti WHERE username = %s AND pwd = %s"
        cursor = db.cursor()
        cursor.execute(sql, (username, password))
        user = cursor.fetchone()

        if user:
            # Se l'utente esiste nel database, registra il nome utente nella sessione
            session['username'] = user[0]
            return redirect('/profilo')
            # return redirect(next or ('/profilo'))
        else:
            print("Errore: credenziali errate")
            return render_template('loginPage.html')
    return render_template('loginPage.html')


@appWebApi.route("/logout")
def logout():
    session['username'] = None
    return redirect("/")



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
    
    print(sql)
    
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            nome_itinerario = row[0]
            nome_categoria = row[1]
            listaItinerariXCategoria.append(Categoria(nome_itinerario, nome_categoria))
    except:
        print ("Error: cannot fetch data")
    return render_template('idee.html',  categoria = categoriaPassata, lista = listaItinerariXCategoria)

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
    
    print(sql)
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
    
@appWebApi.route("/ItinerarioSalvato", methods=["POST"])
def salvaItinerario():
    if not session.get("username"):
        return redirect("/login")
     
    # nuovoItinerario = request.form.get('nuovoItinerario')
    # print(nuovoItinerario)

    # cursor = db.cursor()
    # listaItinerariUtente=[]
    # sql = "SELECT i.nome\
    #     FROM itinerari i\
    #     JOIN utenti_itinerari ui ON i.ID = ui.id_itinerario\
    #     JOIN utenti u ON ui.id_utente = u.ID\
    #     WHERE u.username ='"+nuovoItinerario+"';"


    # print(sql)
    # try:
    #     cursor.execute(sql)
    #     results = cursor.fetchall()
    #     print(results)
    #     for row in results:
    #         nome_itinerario = row[0]
    #         listaItinerariUtente.append(Itinerario(nome_itinerario))

    # except:
    #     print ("Error: cannot fetch data")
    # return redirect("/profilo", lista = listaItinerariUtente)
    return redirect("/profilo")




@appWebApi.route('/registrazione', methods=['POST','GET'])
def registrazione():
    if request.method == 'POST': 

        cursor = db.cursor()
        username = request.form['username']
        email = request.form['email']
        pwd = request.form['password']

        if Utente.query.filter_by(username=username).first():
            return render_template('registrazioneProva.html', error='Username già esistente')

        if Utente.query.filter_by(email=email).first():
            return render_template('registrazioneProva.html', error='Email già esistente')

        try:
            
            sql=("INSERT INTO utenti (username, email, pwd) VALUES ('%s', '%s', '%s');")
            cursor.execute(sql,(username, email, pwd))
            db.commit()
            
            nuovo_utente = Utente(id=id, username=username, email=email, password=pwd)
            db.session.add(nuovo_utente)
            db.session.commit()

            return redirect('/login')
            
        except Exception as e :
            print("Errore durante la creazione dell'utente: {e}")
            traceback.print_exc()
            return render_template('registrazioneProva.html', error = 'Registrazione fallita')
         
    else:
        return render_template('registrazioneProva.html')










# @appWebApi.route('/createUser', methods=['POST'])
# def createUser():
#     cursor = db.cursor()
#     args = request.args

#     username = args.get("username")
#     email = args.get("email")
#     pwd = args.get("password")
    
#     query = "INSERT INTO utenti (username, email, pwd) VALUES ('%s', '%s', '%s');"

#     try:
        
#         cursor.execute(query % (username, email, pwd))
#         db.commit()

#         try:
#             cursor.execute('SELECT * FROM utenti WHERE id = LAST_INSERT_ID();')
#             res = cursor.fetchone()
#             output = Utente(res[0], res[1], res[2], res[3]).__dict__
#         except:
#             print('QUERY_ERROR : Get Utente appena registrato')
#             return "Errore"

#         return render_template('createUser.html')
    
#     except:
#         print('Error: unable to fetch data')
#         return 'Errore'





    
    
    
    
    
    """
    try:
        cursor.execute(sql)
        results = cursor.fetchone()
        
        output = []
        for row in results:
            utente = Utente(row[0], row[1], row[2], row[3])
            output.append(utente.__dict__)
    except:
        print("Error: unable to fetch data")

    return render_template('getUser.html')
"""

#modifica del profilo utente
@appWebApi.route("/modificaProfilo/<int:id>", methods = ['PUT'])
def modificaProfilo(id):
    try:
        new_username = request.form["username"]
        new_email = request.form["email"]
        new_pwd = request.form["password"]

        with db.cursor() as cursor:
            sql= "update utenti set username = %s, email = %s, pwd = %s where id = %s"
            cursor.execute(sql,(new_username, new_email, new_pwd, id))
            db.commit()

            return redirect("/login")
    except Exception as e:
        db.rollback()
        return render_template("Impossibile modificare l'utente")
    

























#--------------------------------------------------------------------------------------------------------------------------------
# Classi database





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











