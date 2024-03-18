from flask import Flask, request
import pymysql
import json

appWebApi = Flask(__name__)
db = pymysql.connect(host="127.0.0.1", user="root", password="password", db="DBPersone", autocommit=True)


class User:
    id = None
    nome = None
    cognome = None

    def __init__(self, id, n, c):
        self.id = id
        self.nome = n
        self.cognome = c



@appWebApi.route("/")
def principale():
    return "ciao qui tutto bene"

@appWebApi.route("/allusers") #GET http://localhost:5000/allusers 
def getAllUsers():
    strjson = json.dumps(listPersona)
    return strjson

@appWebApi.route("/user") #GET http://localhost:5000/user?id=1
def getUserById():
    userid = int(request.args.get('id'))

    for user in listPersona:
        if int(user['id']) == userid:
            return json.dumps(user)
        
    return "None"

@appWebApi.route("/dballpersone")
def getAllPersoneByDB():
    cursor = db.cursor()

    sql = "SELECT * FROM Persone"
    try:
        cursor.execute(sql)
        # Fetch tutti i dati in una lista di liste
        results = None
        results = cursor.fetchall()

        listaUtenti = []

        for row in results:
            id = row[0]
            nome = row[1]
            cognome = row[2]
            listaUtenti.append(User(id, nome, cognome))

    except:
        print ("Error: unable to fecth data")

    return json.dumps(listaUtenti, default=vars)

@appWebApi.route("/logout")
def closeAll():
    db.close()


if __name__ == "__main__":
    appWebApi.run(host='0.0.0.0', port=8000)