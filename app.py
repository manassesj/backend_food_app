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

        cursor.close() 
        return 'Sucess in create tables'
    except:
        return 'An except occurred'


@app.route('/user/insert', methods=['POST'])
def insert():
    # name = request.json['name']
    # password = request.json['password'] 
    data = request.get_json(force=True)
    
    name = data['name']
    password = data['password']
    print("NAME: " + name)
    print("PASSWORD: " + password)
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
        return {}

@app.route('/user/login', methods=['POST'])
def login():
    data = request.get_json(force=True)
    
    name = data['name']
    password = data['password']
    print("NAME: " + name)
    print("PASSWORD: " + password)

    cursor = mysql.connection.cursor()

    cursor.execute('''SELECT `id`, `name`
                    FROM `User`
                    WHERE name = %s''', [name])

    if len(cursor.fetchall()) > 0:
        cursor.execute('''SELECT `id`,`name`, `password`
                    FROM `User`
                    WHERE name = %s AND password = %s''', [name, password])
        user = cursor.fetchone()
        mysql.connection.commit()
        cursor.close() 
        return user
    else:
        cursor.close()
        return {"status": "ERROR"}

#FOOD ROUTES

@app.route('/food/insert', methods=['POST'])
def insertFood():
    data = request.get_json(force=True)

    name = data['name']
    image = data['image']
    description = data['description']
    category_id = data['category_id']
    price = data['price']
    discount = data['discount']
    rating = data['rating']
    
    print("NAME: " + name)
    print("IMAGE: " + image)

    cursor = mysql.connection.cursor()

    cursor.execute('''INSERT INTO `food`(`name`, `image`, `description`, `category_id`, `price`, `discount`, `rating`) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s)''', [name, image, description, category_id, price, discount, rating])


    cursor.execute('''SELECT * FROM `food` 
                    ORDER BY id DESC
                    LIMIT 1''')
    Food = cursor.fetchone()

    mysql.connection.commit()
    cursor.close() 
    return Food

@app.route('/food/getAll', methods=['GET'])
def getAllFoods():

            
    cursor = mysql.connection.cursor()

    query = '''SELECT * 
            FROM `food`
            ORDER BY id ASC'''
    cursor.execute(query)

    foods = cursor.fetchall()
    
    json_foods = {}
        
    for food in foods:
        id = food['id']
        name = food['name']
        image = food['image']
        description = food['description']
        category_id = food['category_id']
        price = food['price']
        discount = food['discount']
        rating = food['rating']

        json_foods[id] = {
            'name' : name,
            'image' : image,
            'description':  description,
            'category_id': category_id,
            'price': price,
            'discount': discount,
            'rating': rating
        }
        print(json_foods)

    mysql.connection.commit()
    cursor.close() 
    return json_foods

if __name__ == '__main__': 
    app.run(host='0.0.0.0', debug=True)
