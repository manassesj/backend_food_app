from flask import request
from flask_mysqldb import MySQL
from config import app, api, mysql

@app.route('/')
def createDbs():
    cursor = mysql.connection.cursor()
    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS `User` 
                        (
                        `id` int(11) NOT NULL AUTO_INCREMENT,
                        `name` varchar(32) NOT NULL,
                        `password` varchar(32) NOT NULL,
                        PRIMARY KEY (`id`)
                        )''')
        return 'Sucess in create tables'
    except:
        return 'An except occurred'


@app.route('/user/insert', methods=['POST'])
def insert():
    name = request.json['name']
    password = request.json['password']

    cursor = mysql.connection.cursor()

    cursor.execute('''SELECT `name`
                    FROM `User`
                    WHERE name = %s''', [name])

    if len(cursor.fetchall()) < 1:
        cursor.execute('''INSERT INTO `User`(`name`, `password`) VALUES (%s, %s)''', [name, password])

        cursor.execute('''SELECT * FROM `User` 
                        ORDER BY id DESC
                        LIMIT 1''')
        user = cursor.fetchone()
        mysql.connection.commit()
        cursor.close() 
        return user 
    else:
        cursor.close()
        return 'Usuario ja existe'

@app.route('/user/login', methods=['POST'])
def login():
    name = request.json['name']
    password = request.json['password']

    cursor = mysql.connection.cursor()

    cursor.execute('''SELECT `name`
                    FROM `User`
                    WHERE name = %s''', [name])

    if len(cursor.fetchall()) > 0:
        cursor.execute('''SELECT `name`, `password`
                    FROM `User`
                    WHERE name = %s AND password = %s''', [name, password])
        mysql.connection.commit()
        cursor.close() 
        return 'OK'
    else:
        cursor.close()
        return 'ERROR'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
