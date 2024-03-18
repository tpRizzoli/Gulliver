import pymysql

MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'password'
MYSQL_DB = 'gulliver'

db = pymysql.connect(host = MYSQL_HOST, user = MYSQL_USER, password = MYSQL_PASSWORD, db = MYSQL_DB)
cursor = db.cursor()

query = '''SELECT i.nome, u.username, u.email
            FROM itinerari AS i
            JOIN utenti_itinerari AS ui ON i.ID = ui.id_itinerario
            JOIN utenti AS u ON ui.id_utente = u.ID;'''

try:
    cursor.execute(query)
    res = cursor.fetchall()

    for row in res:
        iName = row[0]
        uName = row[1]
        uMail = row[2]
        print(iName, uName, uMail)

except:
    print('nope')

db.close()
