# Gulliver Back-End

from flask import Flask, render_template, request, jsonify
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
            tipologia = Tipologia(row[0], row[1])
            output.append( tipologia)

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
            output.append(utente.__dict__)
    except:
        print("Error: unable to fetch data")
    return json.dumps(output, indent=4)



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
                'id_utente' : row[0],
                'utente' : row[1],
                'id_itinerario':row[2],
                'itinerario' : row[3]
            }
            
            
            output.append(dictionary)
    except:
        print("Error: unable to fetch data")
    return json.dumps(output, indent=4)

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


@app.route('/createUser', methods=['POST'])
def inserisci_dati():
        
        try:
            username = request.args.get("username")
            email = request.args.get("email")
            pwd = request.args.get("password")

            with db.cursor() as cursor:
                query = "INSERT INTO utenti (username, email, pwd) VALUES (%s, %s, %s)"
                cursor.execute(query, (username, email, pwd))
                db.commit()
        #riguardare la risposta in json e la query per la visualizzazione del ID 
            response = {'messaggio': 'Dati inseriti con successo nel database'}
            return json.dumps(response)
        
        except Exception as e:
            db.rollback()
            response = {'errore': str(e)}
            return jsonify(response)
    
@app.route("/modificaProfilo/<int:id>", methods = ['PUT'])
def modificaProfilo(id):
    try:
        new_username = request.args.get("username")
        new_email = request.args.get("email")
        new_pwd = request.args.get("password")

        with db.cursor() as cursor:
            sql= "update utenti set username = %s, email = %s, pwd = %s where id = %s"
            cursor.execute(sql,(new_username, new_email, new_pwd, id))
            db.commit()

            u = {
                'id' : id,
                'username' : new_username,
                'email' : new_email,
                'password': new_pwd 
            }

            return json.dumps(u)
    except Exception as e:
        db.rollback()
        return json.dumps({"Message":"Impossibile modificare l'utente"})
#da controllare appena il metodo creazione itinerario è completato   
#@app.route('/delete/<int:id>', methods = ['DELETE'])
#def delete(id):
#   cur = db.connection.cursor()
#   cur.execute("DELETE FROM itineri WHERE id=%s", (id))
#
#   db.connection.commit()
#   return json.dumps({"Messaggio" : "Itinerario eliminato con successo"})
    
@app.route("/findItinerariSuggeriti/", methods=['GET'])
def findItinerariSuggeriti():
    
    categoria_nome = request.args.get('categoria_nome')
    cursor=db.cursor()  
    sql="""SELECT
                c.ID AS categoria_ID,
                c.nome AS categoria_nome,
                i.ID AS itinerario_ID,
                i.nome AS itinerario_nome,
                i.sysDefault AS itinerario_sysDefault,
                l.ID AS luogo_ID,
                l.nome AS luogo_nome
                FROM categorie c
                JOIN luoghi_categorie lc ON c.ID = lc.id_categoria
                JOIN luoghi l ON lc.id_luogo = l.ID
                JOIN attivita_luoghi al ON l.ID = al.id_luogo
                JOIN attivita a ON al.id_attivita = a.ID
                JOIN attivita_itinerari ai ON a.ID = ai.id_attivita
                JOIN itinerari i ON ai.id_itinerario = i.ID
                WHERE c.nome ='""" +categoria_nome+ """' ;"""
    try:
        cursor.execute(sql)
        result=cursor.fetchall()
            
        output=[]

        for row in result:
                u= {
                    "itinerario_id": row[2],
                    "itinerario_nome": row[3],
                    "luogo_id": row[0],
                    "luogo_nome": row[1]
                    }
                output.append(u)
            
        return json.dumps(output, indent=4) 
                   
    except:
        
        return json.dumps({"message": "Error fetching itinerari"}, indent=4)



        
@app.route("/logout")
def closeAll():
    db.close()

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000)
